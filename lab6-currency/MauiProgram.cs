using CurrencyApp.Services;
using CurrencyApp.ViewModels;
using CurrencyApp.Views;
using Microsoft.Extensions.Logging;

namespace CurrencyApp;

public static class MauiProgram
{
	public static MauiApp CreateMauiApp()
	{
		var builder = MauiApp.CreateBuilder();
		builder
			.UseMauiApp<App>()
			.ConfigureFonts(fonts =>
			{
				fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
				fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
			});

		// впровадження залежностей: сервіси, ViewModel та сторінки
		builder.Services.AddSingleton<NbuService>();
		builder.Services.AddSingleton<FavoritesService>();
		builder.Services.AddTransient(sp =>
			new RatesViewModel(sp.GetRequiredService<NbuService>(), sp.GetRequiredService<FavoritesService>(), false));
		builder.Services.AddTransient<ConverterViewModel>();
		builder.Services.AddTransient<DetailsViewModel>();
		builder.Services.AddTransient<RatesPage>();
		builder.Services.AddTransient<ConverterPage>();
		builder.Services.AddTransient<FavoritesPage>();
		builder.Services.AddTransient<DetailsPage>();

#if DEBUG
		builder.Logging.AddDebug();
#endif

		return builder.Build();
	}
}
