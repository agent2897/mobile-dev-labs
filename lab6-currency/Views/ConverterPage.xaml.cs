using CurrencyApp.ViewModels;

namespace CurrencyApp.Views;

public partial class ConverterPage : ContentPage
{
    private readonly ConverterViewModel _vm;

    public ConverterPage(ConverterViewModel vm)
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
