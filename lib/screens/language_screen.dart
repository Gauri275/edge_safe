import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageScreen extends StatefulWidget {
  const LanguageScreen({super.key});

  @override
  State<LanguageScreen> createState() => _LanguageScreenState();
}

class _LanguageScreenState extends State<LanguageScreen> {
  String _selectedLanguage = 'English';

  final List<Map<String, dynamic>> _languages = [
    {
      'name': 'English',
      'native': 'English',
      'code': 'en',
      'flag': '🇬🇧',
    },
    {
      'name': 'Hindi',
      'native': 'हिंदी',
      'code': 'hi',
      'flag': '🇮🇳',
    },
    {
      'name': 'Malayalam',
      'native': 'മലയാളം',
      'code': 'ml',
      'flag': '🇮🇳',
    },
    {
      'name': 'Marathi',
      'native': 'मराठी',
      'code': 'mr',
      'flag': '🇮🇳',
    },
    {
      'name': 'Tamil',
      'native': 'தமிழ்',
      'code': 'ta',
      'flag': '🇮🇳',
    },
    {
      'name': 'Telugu',
      'native': 'తెలుగు',
      'code': 'te',
      'flag': '🇮🇳',
    },
  ];

  @override
  void initState() {
    super.initState();
    _loadLanguage();
  }

  Future<void> _loadLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _selectedLanguage = prefs.getString('language') ?? 'English';
    });
  }

  Future<void> _selectLanguage(String language) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language', language);
    setState(() {
      _selectedLanguage = language;
    });
    if (mounted) {
      Navigator.pop(context, language);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        title: const Text(
          'Select Language',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // Header
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: Colors.teal.shade50,
            child: const Text(
              'Choose your preferred language for the app',
              style: TextStyle(
                fontSize: 14,
                color: Colors.teal,
              ),
              textAlign: TextAlign.center,
            ),
          ),

          // Language List
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _languages.length,
              itemBuilder: (context, index) {
                final language = _languages[index];
                final isSelected = _selectedLanguage == language['name'];

                return GestureDetector(
                  onTap: () => _selectLanguage(language['name']),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: isSelected
                          ? Colors.teal.shade50
                          : Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: isSelected
                            ? Colors.teal
                            : Colors.grey.shade200,
                        width: isSelected ? 2 : 1,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 8,
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        // Flag
                        Text(
                          language['flag'],
                          style: const TextStyle(fontSize: 32),
                        ),
                        const SizedBox(width: 16),

                        // Language Names
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                language['name'],
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: isSelected
                                      ? Colors.teal
                                      : Colors.black,
                                ),
                              ),
                              Text(
                                language['native'],
                                style: TextStyle(
                                  fontSize: 14,
                                  color: isSelected
                                      ? Colors.teal.shade300
                                      : Colors.grey,
                                ),
                              ),
                            ],
                          ),
                        ),

                        // Check Mark
                        if (isSelected)
                          const Icon(
                            Icons.check_circle,
                            color: Colors.teal,
                            size: 28,
                          ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}