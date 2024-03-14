import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:fl_heatmap/fl_heatmap.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Define the dark mode theme with a specific green color
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorSchemeSeed: Colors.green, // Apply green color in dark mode
      ),

      // Force dark mode to be enabled regardless of system theme
      themeMode: ThemeMode
          .dark, // Change this to ThemeMode.system to follow system theme

      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _selectedIndex = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: <Widget>[
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (int index) {
              setState(() {
                _selectedIndex = index;
              });
            },
            labelType: NavigationRailLabelType.all, // Show all labels
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.home),
                label: Text('Main'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.trending_up),
                label: Text('Sales'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.category),
                label: Text('Attributes'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.reviews),
                label: Text('Ratings vs. Stability'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.public),
                label: Text('Geographical'),
              ),
            ],
          ),
          const VerticalDivider(thickness: 1, width: 1),
          // Updated part to switch between pages
          Expanded(
            child: _getPage(_selectedIndex),
          ),
        ],
      ),
    );
  }
}

// Function to return the widget based on selected index
Widget _getPage(int index) {
  switch (index) {
    case 0:
      return const MainPage();
    case 1:
      return const SalesPage();
    case 2:
      return const AttributesPage();
    case 3:
      return const RatingsStabilityPage();
    case 4:
      return const GeographicalPage();
    default:
      return const MainPage(); // Default case to avoid possible index errors
  }
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeading('Sales'),
          _buildDescription(
              'This visual representation is a graph in which the amount of sales and the revenue each month are plotted together in one graph. This visualization could help to inform the company management of their sales volume and revenue per month. This could help them to see whether certain choices in specific months have an effect on their monthly growth. With this information, the management could adjust their current business strategy and choices to optimize their growth.'),
          const SizedBox(height: 16.0),
          _buildHeading('Monthly Transactions per SKU ID'),
          _buildDescription(
              'This bar chart is quite similar to the previous visual presentation. This visual design sets two different kinds of SKU IDs (premium and unlockcharactermanager) next to each other to compare the amount of transactions. Again, this could inform the company to invest in a certain SKU ID to generate more transactions.'),
          const SizedBox(height: 16.0),
          _buildHeading('Crashes and Daily Rating'),
          _buildDescription(
              'This KPI is more focused on the crashes and its impact rather than the amount of transactions '
              'and revenue. As explained above, the daily rating is considered significant as it could increase '
              'potential new customers and maintain their current customers. The amount of crashes that Emerald-IT produces '
              'could influence the rating of their customers. Most customers prefer stability and reliability and do not prefer crashes. '
              'Therefore, to find out if there is a correlation between the amount of daily crashes and daily rating of the customers '
              'could enlighten the significance of a crash-free system. In the current graph, there is not a clear correlation between '
              'crashes and rating, and thus the company could consider to lower or keep the same budget for stability. This could reduce '
              'costs as investing in a more reliable system is not yet necessary, and this creates room for investing in other business decisions.'),
          const SizedBox(height: 16.0),
          _buildHeading('Total Transactions per Country'),
          _buildDescription(
              'This choropleth map shows almost the same information as the previous map; however, it '
              'shows the revenue instead of the amount of transactions. These two maps together could '
              'enlighten the employees if in certain countries the revenue is high but not many transactions '
              'are done, or the other way around.'),
          const SizedBox(height: 16.0),
          _buildHeading('Total Average Rating per Country'),
          _buildDescription(
              'The total average rating by country is illustrated in a geographical scatter plot. The bubble '
              'sizes in each country represent the countries that have a rating, and the color of the bubbles '
              'shows the score. This plot helps to create a visual overview of the countries with satisfied customers '
              'and less happy customers. This is very important as more satisfied customers lead to more transactions '
              'and thus to more growth. As one might see, the countries in Asia and Mid-America rate this company on average '
              'higher than the European countries. This might suggest that the company should invest in their services in Europe '
              'to grow more and maintain their current business approach in Asia.'),
          const SizedBox(height: 16.0),
        ],
      ),
    );
  }

  Widget _buildHeading(String text) {
    return Text(
      text,
      style: const TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
    );
  }

  Widget _buildDescription(String text) {
    return Text(
      text,
      style: const TextStyle(fontSize: 16.0),
    );
  }
}

class SalesPage extends StatelessWidget {
  const SalesPage({super.key});

  @override
  Widget build(BuildContext context) {
    final crossAxisCount =
        MediaQuery.of(context).orientation == Orientation.portrait ? 1 : 2;

    return GridView.count(
      crossAxisCount: crossAxisCount,
      children: const [
        LineChartSample1(),
        LineChartSample2(),
      ],
    );
  }
}

class AttributesPage extends StatelessWidget {
  const AttributesPage({super.key});

  @override
  Widget build(BuildContext context) {
    final crossAxisCount =
        MediaQuery.of(context).orientation == Orientation.portrait ? 1 : 2;

    return GridView.count(
      crossAxisCount: crossAxisCount,
      children: const [
        HeatmapWidget(),
        BarChartSample2(),
      ],
    );
  }
}

class RatingsStabilityPage extends StatelessWidget {
  const RatingsStabilityPage({super.key});

  @override
  Widget build(BuildContext context) {
    _launchURL();
    return const Center(
      child: Text('Redirecting to the ratings visualization...'),
    );
  }

  void _launchURL() async {
    const url = 'https://liacs.leidenuniv.nl/~s3075400/Data_Science_Assignemet_1/HTML_Files/ratings_visualisation.html';
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}

class GeographicalPage extends StatelessWidget {
  const GeographicalPage({super.key});

  @override
  Widget build(BuildContext context) {
    _launchURL();
    return const Center(
      child: Text('Redirecting to the geographical data visualization...'),
    );
  }

  void _launchURL() async {
    const url = 'https://liacs.leidenuniv.nl/~s3075400/Data_Science_Assignemet_1/HTML_Files/map_visualisation.html';
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}

class _LineChart extends StatelessWidget {
  const _LineChart();

  @override
  Widget build(BuildContext context) {
    return LineChart(sampleData1);
  }

  LineChartData get sampleData1 => LineChartData(
        lineTouchData: lineTouchData1,
        gridData: gridData,
        titlesData: titlesData1,
        borderData: borderData,
        lineBarsData: lineBarsData1,
        minX: 7,
        maxX: 12,
        maxY: 28,
        minY: -12,
      );

  LineTouchData get lineTouchData1 => LineTouchData(
        handleBuiltInTouches: true,
        touchTooltipData: LineTouchTooltipData(
          tooltipBgColor: Colors.blueGrey.withOpacity(0.8),
          getTooltipItems: (List<LineBarSpot> touchedSpots) => touchedSpots
              .map(
                (touchedSpot) => LineTooltipItem(
                  '${(touchedSpot.y).toStringAsFixed(2)}%', // Round to 2 decimals and add '%'
                  const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
              )
              .toList(),
        ),
      );

  FlTitlesData get titlesData1 => FlTitlesData(
        bottomTitles: AxisTitles(
          sideTitles: bottomTitles,
        ),
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        topTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
      );

  List<LineChartBarData> get lineBarsData1 => [
        lineChartBarData1_1,
      ];

  Widget bottomTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      fontWeight: FontWeight.bold,
      fontSize: 16,
    );
    Widget text;
    switch (value.toInt()) {
      case 6:
        text = const Text('JUN', style: style);
        break;
      case 7:
        text = const Text('JUL', style: style);
        break;
      case 8:
        text = const Text('AUG', style: style);
        break;
      case 9:
        text = const Text('SEP', style: style);
        break;
      case 10:
        text = const Text('OCT', style: style);
        break;
      case 11:
        text = const Text('NOV', style: style);
        break;
      case 12:
        text = const Text('DEC', style: style);
        break;
      default:
        text = const Text('');
        break;
    }

    return SideTitleWidget(
      axisSide: meta.axisSide,
      space: 10,
      child: text,
    );
  }

  SideTitles get bottomTitles => SideTitles(
        showTitles: true,
        reservedSize: 32,
        interval: 1,
        getTitlesWidget: bottomTitleWidgets,
      );

  FlGridData get gridData => const FlGridData(show: true);

  FlBorderData get borderData => FlBorderData(
        show: true,
        border: Border(
          bottom: BorderSide(color: Colors.green.withOpacity(0.2), width: 4),
          left: BorderSide(color: Colors.green.withOpacity(0.2), width: 4),
          right: const BorderSide(color: Colors.transparent),
          top: const BorderSide(color: Colors.transparent),
        ),
      );

  LineChartBarData get lineChartBarData1_1 => LineChartBarData(
        isCurved: false,
        color: Colors.green,
        barWidth: 8,
        isStrokeCapRound: true,
        dotData: const FlDotData(show: false),
        belowBarData: BarAreaData(show: false),
        spots: const [
          FlSpot(7, 25.759413933087583),
          FlSpot(8, -9.135855147208872),
          FlSpot(9, -7.730943168941473),
          FlSpot(10, -4.832713754646845),
          FlSpot(11, 13.82533482142858),
          FlSpot(12, -0.5423458757200739),
        ],
      );
}

class LineChartSample1 extends StatefulWidget {
  const LineChartSample1({super.key});

  @override
  State<StatefulWidget> createState() => LineChartSample1State();
}

class LineChartSample1State extends State<LineChartSample1> {
  @override
  Widget build(BuildContext context) {
    return const AspectRatio(
      aspectRatio: 1.23,
      child: Stack(
        children: <Widget>[
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              SizedBox(
                height: 37,
              ),
              Text(
                'Monthly Revenue Growth (%)',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(
                height: 37,
              ),
              Expanded(
                child: Padding(
                  padding: EdgeInsets.only(right: 16, left: 6),
                  child: _LineChart(),
                ),
              ),
              SizedBox(
                height: 10,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _LineChart2 extends StatelessWidget {
  const _LineChart2();

  @override
  Widget build(BuildContext context) {
    return LineChart(sampleData2);
  }

  LineChartData get sampleData2 => LineChartData(
        lineTouchData: lineTouchData2,
        gridData: gridData,
        titlesData: titlesData2,
        borderData: borderData,
        lineBarsData: lineBarsData2,
        minX: 7,
        maxX: 12,
        maxY: 28,
        minY: -12,
      );

  LineTouchData get lineTouchData2 => LineTouchData(
        handleBuiltInTouches: true,
        touchTooltipData: LineTouchTooltipData(
          tooltipBgColor: Colors.blueGrey.withOpacity(0.8),
          getTooltipItems: (List<LineBarSpot> touchedSpots) => touchedSpots
              .map(
                (touchedSpot) => LineTooltipItem(
                  '${(touchedSpot.y).toStringAsFixed(2)}%', // Round to 2 decimals and add '%'
                  const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
              )
              .toList(),
        ),
      );

  FlTitlesData get titlesData2 => FlTitlesData(
        bottomTitles: AxisTitles(
          sideTitles: bottomTitles,
        ),
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        topTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
      );

  List<LineChartBarData> get lineBarsData2 => [
        lineChartBarData2_2,
      ];

  Widget bottomTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      fontWeight: FontWeight.bold,
      fontSize: 16,
    );
    Widget text;
    switch (value.toInt()) {
      case 6:
        text = const Text('JUN', style: style);
        break;
      case 7:
        text = const Text('JUL', style: style);
        break;
      case 8:
        text = const Text('AUG', style: style);
        break;
      case 9:
        text = const Text('SEP', style: style);
        break;
      case 10:
        text = const Text('OCT', style: style);
        break;
      case 11:
        text = const Text('NOV', style: style);
        break;
      case 12:
        text = const Text('DEC', style: style);
        break;
      default:
        text = const Text('');
        break;
    }

    return SideTitleWidget(
      axisSide: meta.axisSide,
      space: 10,
      child: text,
    );
  }

  SideTitles get bottomTitles => SideTitles(
        showTitles: true,
        reservedSize: 32,
        interval: 1,
        getTitlesWidget: bottomTitleWidgets,
      );

  FlGridData get gridData => const FlGridData(show: true);

  FlBorderData get borderData => FlBorderData(
        show: true,
        border: Border(
          bottom: BorderSide(color: Colors.green.withOpacity(0.2), width: 4),
          left: BorderSide(color: Colors.green.withOpacity(0.2), width: 4),
          right: const BorderSide(color: Colors.transparent),
          top: const BorderSide(color: Colors.transparent),
        ),
      );

  LineChartBarData get lineChartBarData2_2 => LineChartBarData(
        isCurved: false,
        color: Colors.green,
        barWidth: 8,
        isStrokeCapRound: true,
        dotData: const FlDotData(show: false),
        belowBarData: BarAreaData(show: false),
        spots: const [
          FlSpot(7, 24.782608695652165),
          FlSpot(8, -8.013937282229966),
          FlSpot(9, -11.363636363636365),
          FlSpot(10, -5.555555555555558),
          FlSpot(11, 4.977375565610864),
          FlSpot(12, -1.2931034482758674),
        ],
      );
}

class LineChartSample2 extends StatefulWidget {
  const LineChartSample2({super.key});

  @override
  State<StatefulWidget> createState() => LineChartSample2State();
}

class LineChartSample2State extends State<LineChartSample2> {
  @override
  Widget build(BuildContext context) {
    return const AspectRatio(
      aspectRatio: 1.23,
      child: Stack(
        children: <Widget>[
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              SizedBox(
                height: 37,
              ),
              Text(
                'Monthly Transaction Count Growth (%)',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(
                height: 37,
              ),
              Expanded(
                child: Padding(
                  padding: EdgeInsets.only(right: 16, left: 6),
                  child: _LineChart2(),
                ),
              ),
              SizedBox(
                height: 10,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class HeatmapWidget extends StatefulWidget {
  const HeatmapWidget({super.key});

  @override
  State<HeatmapWidget> createState() => _HeatmapWidgetState();
}

class _HeatmapWidgetState extends State<HeatmapWidget> {
  HeatmapItem? selectedItem;

  late HeatmapData heatmapData;

  @override
  void initState() {
    _initExampleData();
    super.initState();
  }

  void _initExampleData() {
    const columns = [
      'MON',
      'TUE',
      'WED',
      'THU',
      'FRI',
      'SAT',
      'SUN',
    ];
    const rows = [
      'JUN',
      'JUL',
      'AUG',
      'SEP',
      'OCT',
      'NOV',
      'DEC',
    ];
    List<double> values = [
      8,
      28,
      43,
      27,
      29,
      25,
      40,
      26,
      31,
      28,
      48,
      42,
      64,
      48,
      42,
      40,
      21,
      20,
      38,
      39,
      64,
      14,
      18,
      30,
      53,
      37,
      43,
      39,
      37,
      26,
      20,
      27,
      24,
      48,
      39,
      33,
      38,
      26,
      22,
      29,
      39,
      45,
      34,
      20,
      30,
      26,
      36,
      35,
      48,
    ];
    const String unit = 'Transactions';

    List<HeatmapItem> items = [];
    for (int row = 0; row < rows.length; row++) {
      for (int col = 0; col < columns.length; col++) {
        int index = row * columns.length + col;
        items.add(HeatmapItem(
          value: values[index],
          unit: unit,
          xAxisLabel: columns[col],
          yAxisLabel: rows[row],
        ));
      }
    }

    heatmapData = HeatmapData(rows: rows, columns: columns, items: items);
  }

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Text(
              'Transaction count',
              style: TextStyle(
                color: Colors.green,
                fontSize: 32,
                fontWeight: FontWeight.bold,
                letterSpacing: 2,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(
              height: 37,
            ),
            Row(
              children: [
                const Padding(
                  padding: EdgeInsets.only(top: 8.0, bottom: 8.0),
                  child: RotatedBox(
                    quarterTurns: -1,
                    child: Text('Month of the Year'),
                  ),
                ),
                Expanded(
                  child: Heatmap(
                    heatmapData: heatmapData,
                  ),
                ),
              ],
            ),
            const Center(
              child: Padding(
                padding: EdgeInsets.all(8.0),
                child: Text('Day of the Week'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class BarChartSample2 extends StatefulWidget {
  const BarChartSample2({super.key});
  final Color leftBarColor = Colors.green;
  final Color rightBarColor = Colors.lightGreen;

  @override
  State<StatefulWidget> createState() => BarChartSample2State();
}

class BarChartSample2State extends State<BarChartSample2> {
  final double width = 20;

  late List<BarChartGroupData> rawBarGroups;
  late List<BarChartGroupData> showingBarGroups;

  int touchedGroupIndex = -1;

  @override
  void initState() {
    super.initState();
    final barGroup1 = makeGroupData(6, 99, 131);
    final barGroup2 = makeGroupData(7, 121, 166);
    final barGroup3 = makeGroupData(8, 122, 142);
    final barGroup4 = makeGroupData(9, 92, 142);
    final barGroup5 = makeGroupData(10, 87, 134);
    final barGroup6 = makeGroupData(11, 91, 141);
    final barGroup7 = makeGroupData(12, 96, 133);

    final items = [
      barGroup1,
      barGroup2,
      barGroup3,
      barGroup4,
      barGroup5,
      barGroup6,
      barGroup7,
    ];

    rawBarGroups = items;

    showingBarGroups = rawBarGroups;
  }

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                const Text(
                  'Monthly transaction count per SKU ID',
                  style: TextStyle(
                    color: Colors.green,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(
                  height: 37,
                ),
                Expanded(
                  child: BarChart(
                    BarChartData(
                      maxY: 180,
                      titlesData: FlTitlesData(
                        show: true,
                        rightTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                        topTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            getTitlesWidget: bottomTitles,
                            reservedSize: 42,
                          ),
                        ),
                        leftTitles: const AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 42,
                          ),
                        ),
                      ),
                      borderData: FlBorderData(
                        show: false,
                      ),
                      barGroups: showingBarGroups,
                      gridData: const FlGridData(show: true),
                    ),
                  ),
                ),
                const SizedBox(
                  height: 12,
                ),
              ],
            ),
          ),
          Positioned(
            top: 120,
            right: 36,
            child: Card(
              child: LegendsListWidget(
                legends: [
                  Legend('Premium', Colors.green),
                  Legend('Unlockcharactermanager', Colors.lightGreen),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget bottomTitles(double value, TitleMeta meta) {
    final titles = <String>[
      'JUN',
      'JUL',
      'AUG',
      'SEP',
      'OCT',
      'NOV',
      'DEC',
    ];

    final Widget text = Text(
      titles[(value - 6).toInt()],
    );

    return SideTitleWidget(
      axisSide: meta.axisSide,
      space: 16, //margin top
      child: text,
    );
  }

  BarChartGroupData makeGroupData(int x, double y1, double y2) {
    return BarChartGroupData(
      barsSpace: 0,
      x: x,
      barRods: [
        BarChartRodData(
          toY: y1,
          color: widget.leftBarColor,
          width: width,
        ),
        BarChartRodData(
          toY: y2,
          color: widget.rightBarColor,
          width: width,
        ),
      ],
    );
  }
}

class LegendWidget extends StatelessWidget {
  const LegendWidget({
    super.key,
    required this.name,
    required this.color,
  });
  final String name;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 10,
          height: 10,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: color,
          ),
        ),
        const SizedBox(width: 6),
        Text(name),
      ],
    );
  }
}

class LegendsListWidget extends StatelessWidget {
  const LegendsListWidget({
    super.key,
    required this.legends,
  });
  final List<Legend> legends;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 16,
      children: legends
          .map(
            (e) => LegendWidget(
              name: e.name,
              color: e.color,
            ),
          )
          .toList(),
    );
  }
}

class Legend {
  Legend(this.name, this.color);
  final String name;
  final Color color;
}
