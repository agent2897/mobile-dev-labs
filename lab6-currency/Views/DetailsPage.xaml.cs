using CurrencyApp.ViewModels;

namespace CurrencyApp.Views;

public partial class DetailsPage : ContentPage
{
    public DetailsPage(DetailsViewModel vm)
    {
        InitializeComponent();
        BindingContext = vm;
    }
}
