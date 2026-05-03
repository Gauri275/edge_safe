import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../main.dart';
import 'language_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _isDarkMode = false;
  String _cityName = 'Solapur';
  String _backendUrl = 'http://10.0.2.2:5000';
  String _selectedLanguage = 'English';

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _isDarkMode = prefs.getBool('darkMode') ?? false;
      _cityName = prefs.getString('cityName') ?? 'Solapur';
      _backendUrl = prefs.getString('backendUrl') ?? 'http://10.0.2.2:5000';
      _selectedLanguage = prefs.getString('language') ?? 'English';
    });
  }

  Future<void> _saveSetting(String key, dynamic value) async {
    final prefs = await SharedPreferences.getInstance();
    if (value is bool) {
      await prefs.setBool(key, value);
    } else if (value is String) {
      await prefs.setString(key, value);
    }
  }

  void _showEditDialog(String title, String currentValue, String key) {
    final controller = TextEditingController(text: currentValue);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Edit $title'),
        content: TextField(
          controller: controller,
          decoration: InputDecoration(
            hintText: 'Enter $title',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              setState(() {
                if (key == 'cityName') _cityName = controller.text;
                if (key == 'backendUrl') _backendUrl = controller.text;
              });
              _saveSetting(key, controller.text);
              Navigator.pop(context);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.teal,
            ),
            child: const Text(
              'Save',
              style: TextStyle(color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        title: const Text(
          'Settings',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          // App Settings Section
          _buildSectionHeader('App Settings'),
          const SizedBox(height: 8),

          // Dark Mode
          _buildSettingCard(
            child: SwitchListTile(
              title: const Text(
                'Dark Mode',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: const Text('Toggle dark/light theme'),
              secondary: const Icon(Icons.dark_mode, color: Colors.teal),
              value: _isDarkMode,
              activeColor: Colors.teal,
              onChanged: (value) {
                setState(() => _isDarkMode = value);
                _saveSetting('darkMode', value);
                Provider.of<ThemeProvider>(context, listen: false)
                    .toggleTheme(value);
              },
            ),
          ),

          const SizedBox(height: 8),

          // Language
          _buildSettingCard(
            child: ListTile(
              leading: const Icon(Icons.language, color: Colors.teal),
              title: const Text(
                'Language',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: Text(_selectedLanguage),
              trailing: const Icon(Icons.arrow_forward_ios, size: 16),
              onTap: () async {
                final result = await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const LanguageScreen(),
                  ),
                );
                if (result != null) {
                  setState(() => _selectedLanguage = result);
                  _saveSetting('language', result);
                }
              },
            ),
          ),

          const SizedBox(height: 24),

          // Location Settings Section
          _buildSectionHeader('Location Settings'),
          const SizedBox(height: 8),

          // City Name
          _buildSettingCard(
            child: ListTile(
              leading: const Icon(Icons.location_city, color: Colors.teal),
              title: const Text(
                'City Name',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: Text(_cityName),
              trailing: const Icon(Icons.edit, size: 16),
              onTap: () => _showEditDialog('City Name', _cityName, 'cityName'),
            ),
          ),

          const SizedBox(height: 24),

          // Backend Settings Section
          _buildSectionHeader('Backend Settings'),
          const SizedBox(height: 8),

          // Backend URL
          _buildSettingCard(
            child: ListTile(
              leading: const Icon(Icons.cloud, color: Colors.teal),
              title: const Text(
                'Backend URL',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: Text(
                _backendUrl,
                overflow: TextOverflow.ellipsis,
              ),
              trailing: const Icon(Icons.edit, size: 16),
              onTap: () =>
                  _showEditDialog('Backend URL', _backendUrl, 'backendUrl'),
            ),
          ),

          const SizedBox(height: 8),

          // Model Status
          _buildSettingCard(
            child: ListTile(
              leading: const Icon(Icons.memory, color: Colors.teal),
              title: const Text(
                'AI Model Status',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: const Text('Not connected'),
              trailing: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 8,
                  vertical: 4,
                ),
                decoration: BoxDecoration(
                  color: Colors.red.shade100,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  'Offline',
                  style: TextStyle(
                    color: Colors.red.shade700,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),

          const SizedBox(height: 24),

          // About Section
          _buildSectionHeader('About'),
          const SizedBox(height: 8),

          _buildSettingCard(
            child: const ListTile(
              leading: Icon(Icons.info, color: Colors.teal),
              title: Text(
                'EdgeSafe',
                style: TextStyle(fontWeight: FontWeight.w500),
              ),
              subtitle: Text('Version 1.0.0\nYour Emergency Assistant'),
            ),
          ),

          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(
      title,
      style: const TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.bold,
        color: Colors.teal,
      ),
    );
  }

  Widget _buildSettingCard({required Widget child}) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: child,
    );
  }
}