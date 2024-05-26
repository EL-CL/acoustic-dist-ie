calibration_dates = {
    'East Slavic':           760,
    'Czech-Slovak':          1050,
    'Slavic':                1450,
    'Italo-Western Romance': 1524,
    'Balto-Slavic':          3400,
    'Iranian':               3900,
    'Indo-Iranian':          4400,
}
calibration_points = {
    'East Slavic': (
        ('Russian',),
        ('Ukrainian',),
    ),
    'Czech-Slovak': (
        ('Czech',),
        ('Slovak',),
    ),
    'Slavic': (
        ('Polish', 'Czech',  'Slovak',),
        ('Russian', 'Ukrainian',),
        ('Slovenian', 'Serbian', 'Bosnian', 'Croatian', 'Bulgarian', 'Macedonian',),
    ),
    'Italo-Western Romance': (
        ('Portuguese', 'Galician', 'Spanish', 'Catalan', 'French',),
        ('Italian',),
    ),
    'Balto-Slavic': (
        ('Lithuanian', 'Latvian',),
        ('Polish', 'Czech', 'Slovak', 'Russian', 'Ukrainian', 'Slovenian', 'Serbian', 'Bosnian', 'Croatian', 'Bulgarian', 'Macedonian',),
    ),
    'Iranian': (
        ('Persian',),
        ('Pashto',),
    ),
    'Indo-Iranian': (
        ('Persian', 'Pashto',),
        ('Nepali', 'Gujarati', 'Hindi', 'Urdu', 'Marathi', 'Bengali', 'Sinhala',),
    ),
}
prediction_points = {
    'Celtic': (
        ('Irish',),
        ('Welsh',),
    ),
    'Italic': (
        ('Portuguese', 'Galician', 'Spanish', 'Catalan', 'French', 'Italian',),
        ('Romanian',),
    ),
    'Germanic': (
        ('Icelandic', 'Norwegian', 'Swedish', 'Danish',),
        ('English', 'Dutch', 'Afrikaans', 'German',),
    ),
    'Balto-Slavic': (
        ('Lithuanian', 'Latvian',),
        ('Polish', 'Czech', 'Slovak', 'Russian', 'Ukrainian', 'Slovenian', 'Serbian', 'Bosnian', 'Croatian', 'Bulgarian', 'Macedonian',),
    ),
    'Indo-Iranian': (
        ('Persian', 'Pashto',),
        ('Nepali', 'Gujarati', 'Hindi', 'Urdu', 'Marathi', 'Bengali', 'Sinhala',),
    ),
    'Indo-European': (
        ('Irish', 'Welsh',),
        ('Portuguese', 'Galician', 'Spanish', 'Catalan', 'French', 'Italian', 'Romanian',),
        ('Icelandic', 'Norwegian', 'Swedish', 'Danish', 'English', 'Dutch', 'Afrikaans', 'German',),
        ('Lithuanian', 'Latvian', 'Polish', 'Czech', 'Slovak', 'Russian', 'Ukrainian', 'Slovenian', 'Serbian', 'Bosnian', 'Croatian', 'Bulgarian', 'Macedonian',),
        ('Persian', 'Pashto', 'Nepali', 'Gujarati', 'Hindi', 'Urdu', 'Marathi', 'Bengali', 'Sinhala',),
        ('Albanian',),
        ('Greek',),
        ('Armenian',),
    ),
}
