using System.Windows.Input;
using CurrencyApp.Models;
using CurrencyApp.Services;

namespace CurrencyApp.ViewModels;

/// <summary>Сторінка валюти: поточний курс, графік за період, додавання в обране</summary>
public class DetailsViewModel : BaseViewModel, IQueryAttributable
{
    private readonly NbuService _nbu;
    private readonly FavoritesService _favorites;

    private Rate _rate = new();
    public Rate Rate { get => _rate; set => Set(ref _rate, value); }

    private List<RatePoint> _history = new();
    public List<RatePoint> History { get => _history; set => Set(ref _history, value); }

    private int _days = 30;
    public int Days { get => _days; set => Set(ref _days, value); }

    private string _summary = "";
    public string Summary { get => _summary; set => Set(ref _summary, value); }

    private Color _summaryColor = Colors.Gray;
    public Color SummaryColor { get => _summaryColor; set => Set(ref _summaryColor, value); }

    public string FavoriteText => _favorites.Contains(Rate.Cc) ? "★ В обраному" : "☆ Додати в обране";

    public ICommand ToggleFavoriteCommand { get; }
    public ICommand PeriodCommand { get; }

    public DetailsViewModel(NbuService nbu, FavoritesService favorites)
    {
        _nbu = nbu;
        _favorites = favorites;
        ToggleFavoriteCommand = new Command(() =>
        {
            _favorites.Toggle(Rate.Cc);
            OnPropertyChanged(nameof(FavoriteText));
        });
        PeriodCommand = new Command<string>(async d => { Days = int.Parse(d); await LoadHistoryAsync(); });
    }

    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        Rate = (Rate)query["rate"];
        OnPropertyChanged(nameof(FavoriteText));
        _ = LoadHistoryAsync();
    }

    private Task LoadHistoryAsync() => RunAsync(async () =>
    {
        History = await _nbu.GetHistoryAsync(Rate.Cc, Days);
        if (History.Count < 2) { Summary = ""; return; }
        var first = History.First().Value;
        var last = History.Last().Value;
        var diff = last - first;
        var pct = diff / first * 100;
        Summary = $"За {Days} днів: {(diff >= 0 ? "+" : "")}{diff:N2} ₴ ({pct:+0.00;-0.00}%)  ·  " +
                  $"мін {History.Min(p => p.Value):N2}, макс {History.Max(p => p.Value):N2}";
        SummaryColor = diff >= 0 ? Color.FromArgb("#2E7D32") : Color.FromArgb("#C62828");
    });
}
