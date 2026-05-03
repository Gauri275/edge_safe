import 'package:flutter/material.dart';
import 'result_screen.dart';
import '../widgets/voice_button.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _queryController = TextEditingController();
  String _selectedMode = 'AI';

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  void _submitQuery() {
    if (_queryController.text.isEmpty) return;
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ResultScreen(
          query: _queryController.text,
          mode: _selectedMode,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        title: const Text(
          'EdgeSafe',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),

            // Mode Selector
            const Text(
              'Select Mode',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _buildModeButton('AI'),
                const SizedBox(width: 12),
                _buildModeButton('DB'),
              ],
            ),

            const SizedBox(height: 30),

            // Query Input
            const Text(
              'Ask a Question',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _queryController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'e.g. What to do during an earthquake?',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(
                    color: Colors.teal,
                    width: 2,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Submit Button
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: _submitQuery,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.teal,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Get Answer',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.white,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Voice Button
            Center(
              child: VoiceButton(
                onResult: (text) {
                  setState(() {
                    _queryController.text = text;
                  });
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModeButton(String mode) {
    final isSelected = _selectedMode == mode;
    return Expanded(
      child: GestureDetector(
        onTap: () {
          setState(() {
            _selectedMode = mode;
          });
        },
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? Colors.teal : Colors.transparent,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.teal),
          ),
          child: Center(
            child: Text(
              mode == 'AI' ? '🤖 AI Mode' : '🗄️ DB Mode',
              style: TextStyle(
                color: isSelected ? Colors.white : Colors.teal,
                fontWeight: FontWeight.bold,
                fontSize: 16,
              ),
            ),
          ),
        ),
      ),
    );
  }
}