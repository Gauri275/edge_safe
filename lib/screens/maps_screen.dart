import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../utils/constants.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});
  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  String _type = 'flood';
  late WebViewController _controller;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(NavigationDelegate(
        onPageFinished: (_) => setState(() => _loading = false),
      ));
    _loadMap();
  }

  void _loadMap() {
    setState(() => _loading = true);
    _controller.loadRequest(
      Uri.parse('${Constants.baseUrl}/map?type=$_type&city=Solapur'),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Offline Map',
            style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF1A1A2E),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Disaster type filter
          Container(
            height: 50,
            color: Colors.white,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              children: ['flood', 'fire', 'earthquake', 'general']
                  .map((type) => GestureDetector(
                onTap: () {
                  setState(() => _type = type);
                  _loadMap();
                },
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  margin: const EdgeInsets.only(right: 8),
                  padding: const EdgeInsets.symmetric(
                      horizontal: 16, vertical: 4),
                  decoration: BoxDecoration(
                    color: _type == type
                        ? const Color(0xFFE53935)
                        : Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(type,
                      style: TextStyle(
                        color: _type == type
                            ? Colors.white : Colors.grey[700],
                        fontSize: 13, fontWeight: FontWeight.w500,
                      )),
                ),
              ))
                  .toList(),
            ),
          ),

          // Map webview
          Expanded(
            child: Stack(
              children: [
                WebViewWidget(controller: _controller),
                if (_loading)
                  const Center(child: CircularProgressIndicator(
                      color: Color(0xFFE53935))),
              ],
            ),
          ),
        ],
      ),
    );
  }
}