import 'package:flutter/material.dart';

import '../models/expense.dart';

/// Стовпчикова діаграма витрат за категоріями, намальована через CustomPainter
class CategoryBarChart extends StatelessWidget {
  const CategoryBarChart({super.key, required this.data});

  final Map<Category, double> data;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 200,
      child: CustomPaint(
        painter: _BarPainter(data, Theme.of(context).colorScheme.outlineVariant),
        child: Container(),
      ),
    );
  }
}

class _BarPainter extends CustomPainter {
  _BarPainter(this.data, this.gridColor);

  final Map<Category, double> data;
  final Color gridColor;

  @override
  void paint(Canvas canvas, Size size) {
    const iconZone = 28.0;
    final chartH = size.height - iconZone;
    final maxVal = data.values.fold<double>(0, (m, v) => v > m ? v : m);

    final grid = Paint()
      ..color = gridColor
      ..strokeWidth = 1;
    for (var i = 0; i <= 4; i++) {
      final y = chartH * i / 4;
      canvas.drawLine(Offset(0, y), Offset(size.width, y), grid);
    }

    final cats = Category.values;
    final slot = size.width / cats.length;
    for (var i = 0; i < cats.length; i++) {
      final value = data[cats[i]] ?? 0;
      final h = maxVal == 0 ? 0.0 : chartH * value / maxVal;
      final rect = RRect.fromRectAndCorners(
        Rect.fromLTWH(i * slot + slot * 0.2, chartH - h, slot * 0.6, h),
        topLeft: const Radius.circular(6),
        topRight: const Radius.circular(6),
      );
      canvas.drawRRect(rect, Paint()..color = cats[i].color);

      // іконка категорії під стовпчиком
      final icon = cats[i].icon;
      final tp = TextPainter(
        text: TextSpan(
          text: String.fromCharCode(icon.codePoint),
          style: TextStyle(fontSize: 20, fontFamily: icon.fontFamily, package: icon.fontPackage, color: cats[i].color),
        ),
        textDirection: TextDirection.ltr,
      )..layout();
      tp.paint(canvas, Offset(i * slot + (slot - tp.width) / 2, chartH + 6));
    }
  }

  @override
  bool shouldRepaint(_BarPainter old) => old.data != data;
}
