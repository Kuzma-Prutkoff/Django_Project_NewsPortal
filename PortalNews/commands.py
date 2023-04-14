# Создаем 3 юзеров
from news_app.models import *
user_1 = User.objects.create_user(username='Bob')
user_2 = User.objects.create_user(username='Klava')
user_3 = User.objects.create_user(username='Petruha')

# Создаем 3 авторов
Author.objects.create(author_user=user_1)
Author.objects.create(author_user=user_2)
Author.objects.create(author_user=user_3)

# Создаем 4 категории
Category.objects.create(name_category='Sport')
Category.objects.create(name_category='Lawlessness')
Category.objects.create(name_category='Education')
Category.objects.create(name_category='Degradation')

# Создаем 3 поста
author_1 = Author.objects.get(id=1)
Post.objects.create(author=author_1, news_or_article='NW', title='О спорт - ты наше всё', text='Наши олимпийские чемпионы приехали в страну Вануату, где впервые будет проходить зимняя олимпиада. Но на этой олимпиаде им запрещено рекламировать свою гендерную роль в жизни, а потому все они будут бегать в масках и широких комбинезонах, чтобы стрыть свою постыдную гендерную роль. Наш боевой отдел олимпийского комитета подал жалобу на такой беспредел,но как обычно был послан в одиночное пешее эротическое путешествие.')
author_2 = Author.objects.get(id=2)
Post.objects.create(author=author_2, news_or_article='AR', title='Война и мир!!!', text="С сегодняшнего дня запрещено использовать слово 'МИР' в контексте войны. А потому, всеми нами любимое произведение Л.В.Толстого называется теперь так '____ и _'. Дети счастливы!")
author_3 = Author.objects.get(id=3)
Post.objects.create(author=author_3, news_or_article='AR', title='Вперед МакДак. Или наш ответ Чем-Берлену?', text="Всеми нами дорого-нелюбимый МакДак с завтрашнего дня будет переимован либо в 'МосКотлету', либо же в нехитрую абревиатуру 'МММ' - сеть бесплатных туалетов масквы. Говорят, что на открытие первого переименованного МакДак-а приедет сам ПЖ, будем надеяться и верить. А вы уже проголосовали за новое название? Пишите ваши комменты, ставьте лайки и дизлайки.")

# Присваиваем категории постам
Post.objects.get(id=1).post_category.add(Category.objects.get(id=1))
Post.objects.get(id=2).post_category.add(Category.objects.get(id=3))
Post.objects.get(id=2).post_category.add(Category.objects.get(id=2))
Post.objects.get(id=3).post_category.add(Category.objects.get(id=4))

# Создаем 4 коммента
Comment.objects.create(comment_post=Post.objects.get(id=1), comment_user=Author.objects.get(id=1).author_user, comment_text='Я-КРАСАВЧЕГ')
Comment.objects.create(comment_post=Post.objects.get(id=3), comment_user=Author.objects.get(id=1).author_user, comment_text='Я за мос-котлету ++')
Comment.objects.create(comment_post=Post.objects.get(id=3), comment_user=Author.objects.get(id=3).author_user, comment_text='а я за МММ')
Comment.objects.create(comment_post=Post.objects.get(id=2), comment_user=Author.objects.get(id=2).author_user, comment_text='Десять негретят тоже переименовали')

# Ставим лайки дизлайки комментам
Comment.objects.get(id=1).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=1).comment_rating  # 1
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).comment_rating  # -2

#  Ставим лайки дизлайки постам
Post.objects.get(id=1).like()
Post.objects.get(id=2).like()
Post.objects.get(id=2).like()
Post.objects.get(id=3).like()

# Обновляем рейтинги пользователей
author_1.update_rating()
author_1.author_rating # 9
author_2.update_rating()
author_2.author_rating # 12
author_3.update_rating()
author_3.author_rating # 5

# username и рейтинг лучшего пользователя по рейтингу
for i in Author.objects.order_by('-author_rating')[:1]:
    i.author_rating
    i.author_user.username

#дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи(на лайках/дислайках к статье)
for i in Post.objects.order_by('-post_rating')[:1]:
    i.author.author_user.username # Klava
    i.title
    i.post_rating
    i.date_in
    i.preview()

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Post.objects.order_by('-post_rating')[0].comment_set.all().values('comment_user__username', 'time_in', 'comment_rating', 'comment_text')