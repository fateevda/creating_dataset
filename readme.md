# Копрус новостей
Учебный текстовый корпус для курса Корпусная лингвистика.

Данные взяты с сайта https://ria.ru/

## Хранилище корпуса
Каждая новость лежит в отдельном текстовом файле.
Новости разбиты по жанрам.

### Удаление дубликатов
Было удалено 4 дубликата. Пример дубликата находится в duplicate.txt

### Имеется поиск
Так например по запросу "Путин" мы имеем 260 новостей, по запросу "Иран" - 79. А по запросу "Путин и Иран" всего 3.

### Baseline
Our categories: ['В мире', 'Экономика', 'Общество', 'Происшествия']
Size of train: 2669; Size of test 668
We have 4 categories. Accuracy: 0.86

### Словосочетания
Наиболее интересные результаты получены по метрике PMI:
01. hyundai solaris (5)
02. астанинскому формату (5)
03. разведывательного интереса (5)
04. селении экажево (5)
05. тахсин аль-хафаджи (5)
06. little big (6)
07. берутся избирательно (6)
08. джонса хопкинса (6)
09. катаиб хезболлах (6)
10. польских госпиталях (5)
11. приверженность астанинскому (5)
12. топочным мазутом (6)
13. diamond princess (6)
14. new york (7)
15. госчиновникам разного (7)
16. лайнера diamond (6)
17. награжден орденами (7)
18. отечественных разведчиков-нелегалов (7)
19. приморскому краю (6)
20. разведывательных задач (5)  

По словосочетаниям можно понять что было много новостей про Евровидение, конфликту в Сирии и коронавирусу.
