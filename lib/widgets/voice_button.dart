import 'package:flutter/material.dart';
import '../services/stt_service.dart';

class VoiceButton extends StatefulWidget {
  final Function(String) onResult;

  const VoiceButton({
    super.key,
    required this.onResult,
  });

  @override
  State<VoiceButton> createState() => _VoiceButtonState();
}

class _VoiceButtonState extends State<VoiceButton>
    with SingleTickerProviderStateMixin {
  final SttService _sttService = SttService();
  bool _isListening = false;
  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );
    _animation = Tween<double>(begin: 1.0, end: 1.3).animate(
      CurvedAnimation(
        parent: _animationController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _toggleListening() async {
    if (_isListening) {
      await _sttService.stopListening();
      _animationController.stop();
      _animationController.reset();
      setState(() => _isListening = false);
    } else {
      final initialized = await _sttService.initialize();
      if (initialized) {
        await _sttService.startListening(
          onResult: (text) {
            widget.onResult(text);
            _animationController.stop();
            _animationController.reset();
            setState(() => _isListening = false);
          },
        );
        _animationController.repeat(reverse: true);
        setState(() => _isListening = true);
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Microphone not available'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _animation,
      child: GestureDetector(
        onTap: _toggleListening,
        child: Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            color: _isListening ? Colors.red : Colors.teal,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: (_isListening ? Colors.red : Colors.teal)
                    .withValues(alpha: 0.4),
                blurRadius: 12,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Icon(
            _isListening ? Icons.mic : Icons.mic_none,
            color: Colors.white,
            size: 30,
          ),
        ),
      ),
    );
  }
}