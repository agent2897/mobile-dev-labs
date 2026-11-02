using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace CurrencyApp.ViewModels;

/// <summary>Базовий клас ViewModel з реалізацією INotifyPropertyChanged</summary>
public abstract class BaseViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    private bool _isBusy;
    public bool IsBusy { get => _isBusy; set => Set(ref _isBusy, value); }

    private string? _error;
    public string? Error
    {
        get => _error;
        set { Set(ref _error, value); OnPropertyChanged(nameof(HasError)); }
    }
    public bool HasError => !string.IsNullOrEmpty(Error);

    protected bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        OnPropertyChanged(name);
        return true;
    }

    protected void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    /// <summary>Виконує асинхронну дію з індикатором завантаження та обробкою помилки мережі</summary>
    protected async Task RunAsync(Func<Task> action)
    {
        if (IsBusy) return;
        IsBusy = true;
        Error = null;
        try { await action(); }
        catch (Exception) { Error = "Не вдалося завантажити дані. Перевірте з'єднання з Інтернетом."; }
        finally { IsBusy = false; }
    }
}
