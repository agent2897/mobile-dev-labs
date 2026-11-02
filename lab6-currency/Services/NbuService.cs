using System.Net.Http.Json;
using CurrencyApp.Models;

namespace CurrencyApp.Services;

/// <summary>Мережеві запити до відкритого API Національного банку України</summary>
public class NbuService
{
    private const string BaseUrl = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange";
    private readonly HttpClient _http = new() { Timeout = TimeSpan.FromSeconds(20) };
    private List<Rate>? _cache;

    /// <summary>Курси всіх валют на сьогодні (кешуються до примусового оновлення)</summary>
    public async Task<List<Rate>> GetRatesAsync(bool force = false)
    {
        if (_cache != null && !force) return _cache;
        var rates = await _http.GetFromJsonAsync<List<Rate>>($"{BaseUrl}?json") ?? new();
        _cache = rates.OrderBy(r => r.Name).ToList();
        return _cache;
    }

    /// <summary>Історія курсу валюти за останні days днів</summary>
    public async Task<List<RatePoint>> GetHistoryAsync(string cc, int days)
    {
        var to = DateTime.Today;
        var from = to.AddDays(-days + 1);
        var url = $"https://bank.gov.ua/NBU_Exchange/exchange_site?start={from:yyyyMMdd}&end={to:yyyyMMdd}" +
                  $"&valcode={cc.ToLower()}&sort=exchangedate&order=asc&json";
        var items = await _http.GetFromJsonAsync<List<HistoryItem>>(url) ?? new();
        return items
            .Select(i => new RatePoint(DateTime.ParseExact(i.Date, "dd.MM.yyyy", null), i.RatePerUnit))
            .ToList();
    }

    private class HistoryItem
    {
        [System.Text.Json.Serialization.JsonPropertyName("exchangedate")] public string Date { get; set; } = "";
        [System.Text.Json.Serialization.JsonPropertyName("rate_per_unit")] public double RatePerUnit { get; set; }
    }
}
