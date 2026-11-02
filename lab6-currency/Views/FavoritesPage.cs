using CurrencyApp.Services;
using CurrencyApp.ViewModels;

namespace CurrencyApp.Views;

/// <summary>Вкладка «Обране»: той самий список, що й RatesPage, але лише з обраними валютами</summary>
public class FavoritesPage : RatesPage
{
    public FavoritesPage(NbuService nbu, FavoritesService favorites)
        : base(new RatesViewModel(nbu, favorites, onlyFavorites: true)) { }
}
