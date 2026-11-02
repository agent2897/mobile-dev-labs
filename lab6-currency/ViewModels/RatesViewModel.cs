using System.Collections.ObjectModel;
using System.Windows.Input;
using CurrencyApp.Models;
using CurrencyApp.Services;

namespace CurrencyApp.ViewModels;

/// <summary>Список усіх курсів з пошуком; також використовується для вкладки «Обране»</summary>
public class RatesViewModel : BaseViewModel
{
    private readonly NbuService _nbu;
    private readonly FavoritesService _favorites;
    private readonly bool _onlyFavorites;
    private List<Rate> _all = new();

    public ObservableCollection<Rate> Rates { get; } = new();

    private string _search = "";
    public string Search
    {
        get => _search;
        set { if (Set(ref _search, value)) ApplyFilter(); }
    }

    private string _date = "";
    public string Date { get => _date; set => Set(ref _date, value); }

    private bool _isRefreshing;
    public bool IsRefreshing { get => _isRefreshing; set => Set(ref _isRefreshing, value); }

    public bool IsEmpty => !IsBusy && !HasError && Rates.Count == 0;

    public ICommand LoadCommand { get; }
    public ICommand RefreshCommand { get; }
    public ICommand OpenCommand { get; }

    public RatesViewModel(NbuService nbu, FavoritesService favorites, bool onlyFavorites)
    {
        _nbu = nbu;
        _favorites = favorites;
        _onlyFavorites = onlyFavorites;
        LoadCommand = new Command(async () => await LoadAsync(false));
        RefreshCommand = new Command(async () => { await LoadAsync(true); IsRefreshing = false; });
        OpenCommand = new Command<Rate>(async r =>
            await Shell.Current.GoToAsync("details", new Dictionary<string, object> { ["rate"] = r }));
        _favorites.Changed += (_, _) => ApplyFilter();
    }

    private Task LoadAsync(bool force) => RunAsync(async () =>
    {
        _all = await _nbu.GetRatesAsync(force);
        Date = _all.FirstOrDefault()?.ExchangeDate ?? "";
        ApplyFilter();
    });

    private void ApplyFilter()
    {
        var q = Search.Trim();
        var items = _all.Where(r =>
            (!_onlyFavorites || _favorites.Contains(r.Cc)) &&
            (q.Length == 0 || r.Name.Contains(q, StringComparison.OrdinalIgnoreCase) ||
             r.Cc.Contains(q, StringComparison.OrdinalIgnoreCase)));
        Rates.Clear();
        foreach (var r in items) Rates.Add(r);
        OnPropertyChanged(nameof(IsEmpty));
    }
}
