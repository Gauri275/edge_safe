import 'package:flutter/material.dart';
import '../services/tts_service.dart';

class ResultScreen extends StatefulWidget {
  final String query;
  final String mode;

  const ResultScreen({
    super.key,
    required this.query,
    required this.mode,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  bool _isLoading = true;
  bool _isSpeaking = false;
  String _answer = '';
  final TtsService _ttsService = TtsService();

  @override
  void initState() {
    super.initState();
    _getAnswer();
  }

  @override
  void dispose() {
    _ttsService.dispose();
    super.dispose();
  }

  Future<void> _getAnswer() async {
    await Future.delayed(const Duration(seconds: 2));
    setState(() {
      _isLoading = false;
      _answer = widget.mode == 'AI'
          ? 'AI Answer: During an earthquake, drop to your hands and knees, take cover under a sturdy desk or table, and hold on until the shaking stops. Stay away from windows and exterior walls.'
          : 'DB Answer: Standard emergency protocol - Drop, Cover, Hold On. Move away from windows. If outdoors, move to open area away from buildings.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        title: const Text(
          'Result',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Source Badge
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 6,
              ),
              decoration: BoxDecoration(
                color: widget.mode == 'AI'
                    ? Colors.purple.shade100
                    : Colors.blue.shade100,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                widget.mode == 'AI' ? '🤖 AI Response' : '🗄️ DB Response',
                style: TextStyle(
                  color: widget.mode == 'AI'
                      ? Colors.purple
                      : Colors.blue,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Query
            const Text(
              'Your Question:',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              widget.query,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w500,
              ),
            ),

            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 24),

            // Answer
            const Text(
              'Answer:',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 8),

            // Loading or Answer
            _isLoading
                ? const Center(
              child: Column(
                children: [
                  SizedBox(height: 40),
                  CircularProgressIndicator(color: Colors.teal),
                  SizedBox(height: 16),
                  Text('Getting answer...'),
                ],
              ),
            )
                : Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.teal.shade50,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.teal.shade200),
              ),
              child: Text(
                _answer,
                style: const TextStyle(
                  fontSize: 16,
                  height: 1.5,
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Speak Button
            if (!_isLoading)
              SizedBox(
                width: double.infinity,
                height: 50,
                child: OutlinedButton.icon(
                  onPressed: () async {
                    if (_isSpeaking) {
                      await _ttsService.stop();
                      setState(() => _isSpeaking = false);
                    } else {
                      setState(() => _isSpeaking = true);
                      await _ttsService.speak(_answer);
                      setState(() => _isSpeaking = false);
                    }
                  },
                  icon: Icon(
                    _isSpeaking ? Icons.stop : Icons.volume_up,
                    color: Colors.teal,
                  ),
                  label: Text(
                    _isSpeaking ? 'Stop Speaking' : 'Speak Answer',
                    style: const TextStyle(
                      fontSize: 18,
                      color: Colors.teal,
                    ),
                  ),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.teal),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}