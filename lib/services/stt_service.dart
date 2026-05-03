import 'package:speech_to_text/speech_to_text.dart';

class SttService {
  final SpeechToText _speech = SpeechToText();
  bool _isInitialized = false;

  Future<bool> initialize() async {
    _isInitialized = await _speech.initialize(
      onError: (error) => print('STT Error: $error'),
      onStatus: (status) => print('STT Status: $status'),
    );
    return _isInitialized;
  }

  Future<void> startListening({
    required Function(String) onResult,
    String localeId = 'en_IN',
  }) async {
    if (!_isInitialized) await initialize();
    if (_speech.isAvailable) {
      await _speech.listen(
        onResult: (result) {
          if (result.finalResult) {
            onResult(result.recognizedWords);
          }
        },
        localeId: localeId,
      );
    }
  }

  Future<void> stopListening() async {
    await _speech.stop();
  }

  bool get isListening => _speech.isListening;
}