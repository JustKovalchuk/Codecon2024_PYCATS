class Question:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer


questions_texts = ["Як оформити ВПО?", "Як можливо отримати грошову допомогу?", "Що таке ВПОHelpBot?", "Як використовувати бота волонтерам?"]
answers_texts = [
    "\t📝Подати заявку можна як онлайн за кілька кліків у застосунку Дія, так і офлайн за місцем проживання у найближчому ЦНАПі чи органах соціального захисту.\n"
    "\t👨‍👩‍👧З 14 років це можна робити самостійно, від імені дитини мають подавати заявку батьки. Якщо людина є недієздатною або має обмежену дієздатність — від її імені документи подає законний представник.\n"
    "\t📌Детальну інструкцію щодо оформлення ВПО як онлайн так і офлайн можна знайти натиснувши на кнопку нижче👇",

    "\t🏠Компетентні особи, які змушені були залишити свої домівки і переїхати до більш безпечних регіонів в межах України, можуть отримати допомогу як від держави, так і від окремих благодійних організацій.\n"
    "\t🔖Для отримання підтримки з боку держави особам необхідно оформити статус внутрішньо переміщеної особи (ВПО) та обрати картку ЄПідтримка. Детальна інструкція доступна за вказаним посиланням нижче. Щодо отримання допомоги від благодійних фондів, необхідно подати заявку до кожного з них. Список рекомендованих благодійних організацій наведено нижче👇",
    
    "\t🤖ВПОРHelpBot -- сервіз створений для допомоги ВПО та волонтерам, розроблений студентами ЛНУ Івана Франка. Це загальна база даних, яка збирає інформацію про волонтерські події та допомогу ВПО в одному зручному місці.\n "
    "\t🔍На ньому ви можете знайти таку інформацію, як найближчі волонтерські події, різні благодійні фонди та місця проживання для ВПО.\n"
    "\t🚀Бот знаходиться на етапі активного розвитку, ви можете підтримати розробку поширивши його серед знайомих, та поділившись вашими ідеями з розробниками: @yurasov_volodymyr",

    "\t🤖ВПОHelpBot надає доступ до широкого обсягу інформації про актуальні волонтерські ініціативи, з можливістю використання фільтрів за містами. Крім того, бот надає посилання на різні благодійні фонди, де ви можете надавати фінансову підтримку як військовослужбовцям, так і особам, які постраждали від воєнних дій."
    ]
Link = [
    'https://novy.tv/ua/g-space/layfhaki/2022/09/01/yak-oformyty-vpo-u-dodatku-diya-pokrokova-instrukcziya-ta-sluzhba-pidtrymky/',
    'https://ukraine.un.org/uk/185168-%D0%B1%D0%B0%D0%B3%D0%B0%D1%82%D0%BE%D1%86%D1%96%D0%BB%D1%8C%D0%BE%D0%B2%D0%B0-%D0%B3%D1%80%D0%BE%D1%88%D0%BE%D0%B2%D0%B0-%D0%B4%D0%BE%D0%BF%D0%BE%D0%BC%D0%BE%D0%B3%D0%B0-%D1%96%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D1%96%D1%8F-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BB%D0%BE%D0%B3%D0%BE-%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F',
    None,
    None,]

questions_list = {i: Question(i, q, a) for i, (q, a) in enumerate(zip(questions_texts, answers_texts))}


def get_question_by_id(id):
    return questions_list.get(id)
