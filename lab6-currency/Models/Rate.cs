using System.Text.Json.Serialization;

namespace CurrencyApp.Models;

/// <summary>Курс валюти з API НБУ</summary>
public class Rate
{
    [JsonPropertyName("r030")] public int Code { get; set; }
    [JsonPropertyName("txt")] public string Name { get; set; } = "";
    [JsonPropertyName("rate")] public double Value { get; set; }
    [JsonPropertyName("cc")] public string Cc { get; set; } = "";
    [JsonPropertyName("exchangedate")] public string ExchangeDate { get; set; } = "";

    /// <summary>Прапор країни за кодом валюти (для основних валют)</summary>
    public string Flag => Cc switch
    {
        "USD" => "🇺🇸", "EUR" => "🇪🇺", "GBP" => "🇬🇧", "PLN" => "🇵🇱", "CHF" => "🇨🇭",
        "CZK" => "🇨🇿", "JPY" => "🇯🇵", "CNY" => "🇨🇳", "CAD" => "🇨🇦", "TRY" => "🇹🇷",
        "AUD" => "🇦🇺", "SEK" => "🇸🇪", "NOK" => "🇳🇴", "DKK" => "🇩🇰", "HUF" => "🇭🇺",
        "MDL" => "🇲🇩", "GEL" => "🇬🇪", "KZT" => "🇰🇿", "ILS" => "🇮🇱", "INR" => "🇮🇳",
        "KRW" => "🇰🇷", "RON" => "🇷🇴", "AZN" => "🇦🇿", "BGN" => "🇧🇬", "XAU" => "🥇",
        "XAG" => "🥈", "XPT" => "⚪", "XPD" => "⚪",
        _ => "💱",
    };

    public string ValueText => Value.ToString(Value < 1 ? "0.0000" : "0.00");
}

/// <summary>Точка для графіка історії курсу</summary>
public record RatePoint(DateTime Date, double Value);
