using System.Collections.ObjectModel;
using System.Globalization;
using System.Windows.Input;
using CurrencyApp.Models;
using CurrencyApp.Services;

namespace CurrencyApp.ViewModels;

/// <summary>Конвертер між будь-якими двома валютами (включно з гривнею) за курсом НБУ</summary>
public class ConverterViewModel : BaseViewModel
{
    private static readonly Rate Uah = new() { Cc = "UAH", Name = "Українська гривня", Value = 1 };
    private readonly NbuService _nbu;

    public ObservableCollection<Rate> Currencies { get; } = new();

    private Rate? _from;
    public Rate? From { get => _from; set { if (Set(ref _from, value)) Recalc(); } }

    private Rate? _to;
    public Rate? To { get => _to; set { if (Set(ref _to, value)) Recalc(); } }

    private string _amount = "100";
    public string Amount { get => _amount; set { if (Set(ref _amount, value)) Recalc(); } }

    private string _result = "";
    public string Result { get => _result; set => Set(ref _result, value); }

    private string _rateInfo = "";
    public string RateInfo { get => _rateInfo; set => Set(ref _rateInfo, value); }

    public ICommand LoadCommand { get; }
    public ICommand SwapCommand { get; }

    public ConverterViewModel(NbuService nbu)
    {
        _nbu = nbu;
        LoadCommand = new Command(async () => await RunAsync(LoadAsync));
        SwapCommand = new Command(() => (From, To) = (To, From));
    }

    private async Task LoadAsync()
    {
        if (Currencies.Count > 0) return;
        var rates = await _nbu.GetRatesAsync();
        Currencies.Add(Uah);
        foreach (var r in rates.OrderBy(r => r.Cc)) Currencies.Add(r);
        From = Currencies.First(c => c.Cc == "USD");
        To = Uah;
    }

    private void Recalc()
    {
        if (From == null || To == null) return;
        var text = Amount.Replace(',', '.');
        if (!double.TryParse(text, NumberStyles.Float, CultureInfo.InvariantCulture, out var amount) || amount < 0)
        {
            Result = "—";
            RateInfo = "Введіть коректну суму";
            return;
        }
        var cross = From.Value / To.Value; // скільки одиниць To за 1 одиницю From
        Result = $"{amount * cross:N2} {To.Cc}";
        RateInfo = $"1 {From.Cc} = {cross:N4} {To.Cc}";
    }
}
