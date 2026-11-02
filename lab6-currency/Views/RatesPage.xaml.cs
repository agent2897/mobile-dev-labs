using CurrencyApp.ViewModels;

namespace CurrencyApp.Views;

public partial class RatesPage : ContentPage
{
    private readonly RatesViewModel _vm;

    public RatesPage(RatesViewModel vm)
    {
        InitializeComponent();
        BindingContext = _vm = vm;
    }

    protected override void OnAppearing()
    {
        base.OnAppearing();
        _vm.LoadCommand.Execute(null);
    }
}
