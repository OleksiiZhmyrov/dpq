import xlwt

STORY_KEY_STYLE = xlwt.easyxf('font: name Calibri, height 320;'
                              'alignment: horizontal center, vertical center;'
                              'borders: top thick, right medium, bottom medium, left thick;')

STORY_KEY_STYLE_DESK_CHECK = xlwt.easyxf('font: name Calibri, height 320;'
                                         'alignment: horizontal center, vertical center;'
                                         'borders: top thick, right medium, bottom medium, left thick;'
                                         'pattern: pattern solid, pattern_fore_colour green, pattern_back_colour green;')

SUMMARY_STYLE = xlwt.easyxf('font: name Calibri, height 280;'
                            'alignment: horizontal center, vertical center, wrap on;'
                            'borders: top thick, right thick, bottom medium, left medium;')

DESCRIPTION_STYLE = xlwt.easyxf('font: name Calibri, height 240;'
                                'alignment: horizontal center, vertical center, wrap on;'
                                'borders: top medium, right thick, bottom medium, left thick;')

ASSIGNEE_LABEL_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                                   'alignment: horizontal right, vertical center;'
                                   'borders: top medium, right thin, bottom thin, left thick;')

ASSIGNEE_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                             'alignment: horizontal center, vertical center;'
                             'borders: top medium, right medium, bottom thin, left thin;')

TESTER_LABEL_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                                 'alignment: horizontal right, vertical center;'
                                 'borders: top thin, right thin, bottom thin, left thick;')

TESTER_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                           'alignment: horizontal center, vertical center;'
                           'borders: top thin, right medium, bottom thin, left thin;')

REPORTER_LABEL_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                                   'alignment: horizontal right, vertical center;'
                                   'borders: top thin, right thin, bottom medium, left thick;')

REPORTER_STYLE = xlwt.easyxf('font: name Calibri, height 220;'
                             'alignment: horizontal center, vertical center;'
                             'borders: top thin, right medium, bottom medium, left thin;')

STORY_POINTS_STYLE = xlwt.easyxf('font: name Calibri, height 320;'
                                 'alignment: horizontal center, vertical center;'
                                 'borders: top medium, right thick, bottom medium, left medium;')

EPIC_STYLE = xlwt.easyxf('font: name Calibri, height 240;'
                         'alignment: horizontal center, vertical center, wrap on;'
                         'borders: top medium, right thick, bottom thick, left thick;')

