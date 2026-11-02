using CurrencyApp.Views;

namespace CurrencyApp;

public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        // сторінка деталей відкривається поверх вкладок (стекова навігація Shell)
        Routing.RegisterRoute("details", typeof(DetailsPage));
    }
}
