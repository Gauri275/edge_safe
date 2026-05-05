import 'package:flutter/material.dart';

class FirstAidScreen extends StatefulWidget {
  const FirstAidScreen({super.key});

  @override
  State<FirstAidScreen> createState() => _FirstAidScreenState();
}

class _FirstAidScreenState extends State<FirstAidScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = '';

  final List<Map<String, dynamic>> _topics = [
    {
      'title': 'Earthquake',
      'icon': Icons.public,
      'color': Colors.brown,
      'steps': [
        'Drop to your hands and knees',
        'Take cover under a sturdy desk or table',
        'Hold on until shaking stops',
        'Stay away from windows',
        'If outdoors move to open area',
      ],
    },
    {
      'title': 'Flood',
      'icon': Icons.water,
      'color': Colors.blue,
      'steps': [
        'Move to higher ground immediately',
        'Avoid walking in moving water',
        'Do not drive through flooded areas',
        'Disconnect electrical appliances',
        'Listen to emergency broadcasts',
      ],
    },
    {
      'title': 'Fire',
      'icon': Icons.local_fire_department,
      'color': Colors.red,
      'steps': [
        'Call emergency services immediately',
        'Crawl low under smoke',
        'Close doors to slow fire spread',
        'Never use elevator during fire',
        'Meet at designated assembly point',
      ],
    },
    {
      'title': 'CPR',
      'icon': Icons.favorite,
      'color': Colors.pink,
      'steps': [
        'Check if person is responsive',
        'Call emergency services',
        'Begin chest compressions',
        'Push hard and fast 100-120 times per minute',
        'Give rescue breaths if trained',
      ],
    },
    {
      'title': 'Bleeding',
      'icon': Icons.healing,
      'color': Colors.red.shade800,
      'steps': [
        'Apply direct pressure to wound',
        'Use clean cloth or bandage',
        'Keep pressure for 15 minutes',
        'Do not remove cloth if soaked',
        'Elevate injured area if possible',
      ],
    },
    {
      'title': 'Burns',
      'icon': Icons.wb_sunny,
      'color': Colors.orange,
      'steps': [
        'Cool burn with cool running water',
        'Do not use ice or butter',
        'Cover with clean bandage',
        'Do not break blisters',
        'Seek medical help for severe burns',
      ],
    },
    {
      'title': 'Cyclone',
      'icon': Icons.air,
      'color': Colors.teal,
      'steps': [
        'Stay indoors away from windows',
        'Move to interior room',
        'Keep emergency kit ready',
        'Listen to weather updates',
        'Do not go outside during eye of storm',
      ],
    },
    {
      'title': 'Snake Bite',
      'icon': Icons.pest_control,
      'color': Colors.green.shade800,
      'steps': [
        'Keep victim calm and still',
        'Remove tight clothing near bite',
        'Do not suck out venom',
        'Do not apply tourniquet',
        'Rush to hospital immediately',
      ],
    },
  ];

  List<Map<String, dynamic>> get _filteredTopics {
    if (_searchQuery.isEmpty) return _topics;
    return _topics
        .where((topic) => topic['title']
        .toString()
        .toLowerCase()
        .contains(_searchQuery.toLowerCase()))
        .toList();
  }

  void _showTopicDetails(Map<String, dynamic> topic) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        maxChildSize: 0.9,
        minChildSize: 0.4,
        expand: false,
        builder: (context, scrollController) => SingleChildScrollView(
          controller: scrollController,
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Handle bar
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey.shade300,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Title
                Row(
                  children: [
                    Icon(
                      topic['icon'],
                      color: topic['color'],
                      size: 32,
                    ),
                    const SizedBox(width: 12),
                    Text(
                      topic['title'],
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Steps
                const Text(
                  'Emergency Steps:',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey,
                  ),
                ),
                const SizedBox(height: 12),
                ...List.generate(
                  (topic['steps'] as List).length,
                      (index) => Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: BoxDecoration(
                            color: topic['color'],
                            shape: BoxShape.circle,
                          ),
                          child: Center(
                            child: Text(
                              '${index + 1}',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            topic['steps'][index],
                            style: const TextStyle(fontSize: 16),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
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
          'First Aid',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // Search Bar
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _searchController,
              onChanged: (value) {
                setState(() {
                  _searchQuery = value;
                });
              },
              decoration: InputDecoration(
                hintText: 'Search first aid topics...',
                prefixIcon: const Icon(Icons.search, color: Colors.teal),
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
          ),

          // Topics Grid
          Expanded(
            child: _filteredTopics.isEmpty
                ? const Center(
              child: Text(
                'No topics found',
                style: TextStyle(fontSize: 18, color: Colors.grey),
              ),
            )
                : GridView.builder(
              padding: const EdgeInsets.all(16),
              gridDelegate:
              const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.2,
              ),
              itemCount: _filteredTopics.length,
              itemBuilder: (context, index) {
                final topic = _filteredTopics[index];
                return GestureDetector(
                  onTap: () => _showTopicDetails(topic),
                  child: Container(
                    decoration: BoxDecoration(
                      color: (topic['color'] as Color).withValues(
                        alpha: 0.1,
                      ),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: (topic['color'] as Color).withValues(
                          alpha: 0.3,
                        ),
                      ),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          topic['icon'],
                          color: topic['color'],
                          size: 48,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          topic['title'],
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: topic['color'],
                          ),
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