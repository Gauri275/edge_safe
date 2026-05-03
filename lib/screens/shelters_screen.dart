import 'package:flutter/material.dart';

class SheltersScreen extends StatefulWidget {
  const SheltersScreen({super.key});

  @override
  State<SheltersScreen> createState() => _SheltersScreenState();
}

class _SheltersScreenState extends State<SheltersScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = '';

  final List<Map<String, dynamic>> _shelters = [
    {
      'name': 'Government School Shelter',
      'address': 'Near Main Road, Solapur',
      'distance': '1.2 km',
      'capacity': 500,
      'available': 320,
      'type': 'flood',
      'contact': '1800-123-456',
    },
    {
      'name': 'Community Hall',
      'address': 'Market Area, Solapur',
      'distance': '2.5 km',
      'capacity': 300,
      'available': 150,
      'type': 'earthquake',
      'contact': '1800-123-457',
    },
    {
      'name': 'Sports Complex',
      'address': 'Stadium Road, Solapur',
      'distance': '3.1 km',
      'capacity': 800,
      'available': 600,
      'type': 'general',
      'contact': '1800-123-458',
    },
    {
      'name': 'Temple Hall',
      'address': 'Temple Street, Solapur',
      'distance': '0.8 km',
      'capacity': 200,
      'available': 180,
      'type': 'flood',
      'contact': '1800-123-459',
    },
    {
      'name': 'College Auditorium',
      'address': 'College Road, Solapur',
      'distance': '4.2 km',
      'capacity': 1000,
      'available': 750,
      'type': 'general',
      'contact': '1800-123-460',
    },
  ];

  List<Map<String, dynamic>> get _filteredShelters {
    if (_searchQuery.isEmpty) return _shelters;
    return _shelters
        .where((shelter) =>
    shelter['name']
        .toString()
        .toLowerCase()
        .contains(_searchQuery.toLowerCase()) ||
        shelter['address']
            .toString()
            .toLowerCase()
            .contains(_searchQuery.toLowerCase()))
        .toList();
  }

  Color _getCapacityColor(int available, int total) {
    final ratio = available / total;
    if (ratio > 0.5) return Colors.green;
    if (ratio > 0.2) return Colors.orange;
    return Colors.red;
  }

  void _showShelterDetails(Map<String, dynamic> shelter) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
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

            // Name
            Text(
              shelter['name'],
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),

            // Address
            Row(
              children: [
                const Icon(Icons.location_on, color: Colors.teal, size: 18),
                const SizedBox(width: 4),
                Text(
                  shelter['address'],
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Capacity Bar
            const Text(
              'Capacity',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 16,
              ),
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(
              value: shelter['available'] / shelter['capacity'],
              backgroundColor: Colors.grey.shade200,
              color: _getCapacityColor(
                shelter['available'],
                shelter['capacity'],
              ),
              minHeight: 10,
              borderRadius: BorderRadius.circular(5),
            ),
            const SizedBox(height: 4),
            Text(
              '${shelter['available']} / ${shelter['capacity']} spots available',
              style: const TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 16),

            // Contact
            Row(
              children: [
                const Icon(Icons.phone, color: Colors.teal, size: 18),
                const SizedBox(width: 4),
                Text(
                  shelter['contact'],
                  style: const TextStyle(fontSize: 16),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Buttons
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.directions, color: Colors.white),
                    label: const Text(
                      'Directions',
                      style: TextStyle(color: Colors.white),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.teal,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.phone, color: Colors.teal),
                    label: const Text(
                      'Call',
                      style: TextStyle(color: Colors.teal),
                    ),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      side: const BorderSide(color: Colors.teal),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
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
          'Shelters',
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
                hintText: 'Search shelters...',
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

          // Shelter Count
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              children: [
                Text(
                  '${_filteredShelters.length} shelters found',
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),

          // Shelter List
          Expanded(
            child: _filteredShelters.isEmpty
                ? const Center(
              child: Text(
                'No shelters found',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.grey,
                ),
              ),
            )
                : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _filteredShelters.length,
              itemBuilder: (context, index) {
                final shelter = _filteredShelters[index];
                return GestureDetector(
                  onTap: () => _showShelterDetails(shelter),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 8,
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(
                              Icons.home,
                              color: Colors.teal,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                shelter['name'],
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 8,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.teal.shade50,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                shelter['distance'],
                                style: const TextStyle(
                                  color: Colors.teal,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            const Icon(
                              Icons.location_on,
                              color: Colors.grey,
                              size: 14,
                            ),
                            const SizedBox(width: 4),
                            Text(
                              shelter['address'],
                              style: const TextStyle(
                                color: Colors.grey,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        // Capacity
                        Row(
                          children: [
                            const Icon(
                              Icons.people,
                              color: Colors.grey,
                              size: 14,
                            ),
                            const SizedBox(width: 4),
                            Text(
                              '${shelter['available']}/${shelter['capacity']} available',
                              style: const TextStyle(
                                fontSize: 13,
                                color: Colors.grey,
                              ),
                            ),
                            const Spacer(),
                            Container(
                              width: 100,
                              height: 6,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(3),
                                color: Colors.grey.shade200,
                              ),
                              child: FractionallySizedBox(
                                alignment: Alignment.centerLeft,
                                widthFactor: shelter['available'] /
                                    shelter['capacity'],
                                child: Container(
                                  decoration: BoxDecoration(
                                    borderRadius:
                                    BorderRadius.circular(3),
                                    color: _getCapacityColor(
                                      shelter['available'],
                                      shelter['capacity'],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
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