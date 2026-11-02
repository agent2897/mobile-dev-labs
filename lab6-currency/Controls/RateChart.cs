using CurrencyApp.Models;

namespace CurrencyApp.Controls;

/// <summary>Лінійний графік історії курсу, намальований через GraphicsView</summary>
public class RateChart : GraphicsView
{
    public static readonly BindableProperty PointsProperty = BindableProperty.Create(
        nameof(Points), typeof(List<RatePoint>), typeof(RateChart), new List<RatePoint>(),
        propertyChanged: (b, _, _) => ((RateChart)b).Invalidate());

    public List<RatePoint> Points
    {
        get => (List<RatePoint>)GetValue(PointsProperty);
        set => SetValue(PointsProperty, value);
    }

    public RateChart()
    {
        Drawable = new ChartDrawable(this);
    }

    private class ChartDrawable(RateChart owner) : IDrawable
    {
        public void Draw(ICanvas canvas, RectF rect)
        {
            var pts = owner.Points;
            if (pts == null || pts.Count < 2) return;

            const float left = 52, bottom = 26, top = 10;
            var w = rect.Width - left - 8;
            var h = rect.Height - bottom - top;
            var min = pts.Min(p => p.Value);
            var max = pts.Max(p => p.Value);
            if (max - min < 1e-9) { max += 1; min -= 1; }

            // сітка та підписи значень
            canvas.FontSize = 11;
            canvas.FontColor = Colors.Gray;
            canvas.StrokeColor = Color.FromArgb("#E0E0E0");
            canvas.StrokeSize = 1;
            for (var i = 0; i <= 4; i++)
            {
                var y = top + h * i / 4;
                canvas.DrawLine(left, y, left + w, y);
                var v = max - (max - min) * i / 4;
                canvas.DrawString(v.ToString("N2"), 0, y - 8, left - 6, 16, HorizontalAlignment.Right, VerticalAlignment.Center);
            }

            PointF Map(int i) => new(
                left + w * i / (pts.Count - 1),
                top + (float)((max - pts[i].Value) / (max - min)) * h);

            // заливка під лінією
            var area = new PathF();
            area.MoveTo(left, top + h);
            for (var i = 0; i < pts.Count; i++) area.LineTo(Map(i));
            area.LineTo(left + w, top + h);
            area.Close();
            canvas.FillColor = Color.FromArgb("#33512BD4");
            canvas.FillPath(area);

            // лінія графіка
            var line = new PathF();
            line.MoveTo(Map(0));
            for (var i = 1; i < pts.Count; i++) line.LineTo(Map(i));
            canvas.StrokeColor = Color.FromArgb("#512BD4");
            canvas.StrokeSize = 3;
            canvas.StrokeLineJoin = LineJoin.Round;
            canvas.DrawPath(line);

            var last = Map(pts.Count - 1);
            canvas.FillColor = Color.FromArgb("#512BD4");
            canvas.FillCircle(last, 5);

            // підписи дат: перша, середня, остання
            foreach (var i in new[] { 0, pts.Count / 2, pts.Count - 1 })
            {
                var x = Math.Clamp(Map(i).X - 30, 0, rect.Width - 60);
                canvas.DrawString(pts[i].Date.ToString("dd.MM"), x, top + h + 6, 60, 16,
                    HorizontalAlignment.Center, VerticalAlignment.Top);
            }
        }
    }
}
