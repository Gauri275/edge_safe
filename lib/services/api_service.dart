import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static Future<Map<String, dynamic>> getAnswer(String query, String mode) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      // Use Port 5001 as we configured in the backend
      final baseUrl = prefs.getString('backendUrl') ?? 'http://localhost:5001';

      print('Connecting to Backend: $baseUrl/ask');

      final response = await http.post(
        Uri.parse('$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'query': query,
          'mode': mode.toLowerCase(),
          'lang': 'en',
          'city': 'Solapur',
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {
          'answer': 'Error: Server returned status ${response.statusCode}',
          'source': 'error',
        };
      }
    } catch (e) {
      print('Connection Error: $e');
      return {
        'answer': 'Error: Could not connect to backend at Port 5001.\n\nMake sure the backend is running (python app.py).',
        'source': 'error',
      };
    }
  }
}
