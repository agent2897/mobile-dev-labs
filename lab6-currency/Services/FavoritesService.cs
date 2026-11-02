namespace CurrencyApp.Services;

/// <summary>Обрані валюти, зберігаються в Preferences між запусками</summary>
public class FavoritesService
{
    private const string Key = "favorites";
    private readonly HashSet<string> _items;

    public event EventHandler? Changed;

    public FavoritesService()
    {
        var saved = Preferences.Default.Get(Key, "USD,EUR");
        _items = saved.Split(',', StringSplitOptions.RemoveEmptyEntries).ToHashSet();
    }

    public IReadOnlyCollection<string> Items => _items;

    public bool Contains(string cc) => _items.Contains(cc);

    public void Toggle(string cc)
    {
        if (!_items.Remove(cc)) _items.Add(cc);
        Preferences.Default.Set(Key, string.Join(',', _items));
        Changed?.Invoke(this, EventArgs.Empty);
    }
}
