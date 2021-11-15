import json
import re
from selenium import webdriver

from barbook_app.models.stuff import (
    Cocktail,
    Ingredient,
    TagForIngredient,
    TagForCocktail,
    ClassForCocktailTag,
    ClassForIngredientTag,
    BarTool,
    CocktailRecipe,
    CocktailTool,
)

PATH_TO_DRIVER = ""

def get_ing_tags_and_classes():
    browser = webdriver.Chrome(PATH_TO_DRIVER)
    browser.get("https://ru.inshaker.com/goods")
    for el in browser.find_elements_by_class_name("filter-select"):
        class_tag = ClassForIngredientTag(class_name=el.text.lower())
        check = ClassForIngredientTag.objects.filter(class_name=el.text.lower())
        if not check:
            class_tag.save()
        else:
            print(check)
            class_tag = check[0]
        for element in el.find_elements_by_class_name("list"):
            for div in element.find_elements_by_class_name("item"):
                for span in div.find_elements_by_tag_name("span"):
                    print(class_tag.class_name)
                    # check = TagForIngredient.objects.filter(tag_name=span.get_attribute("innerText"))
                    try:
                        tag = TagForIngredient.objects.update_or_create(
                            class_name=class_tag,
                            tag_name=span.get_attribute("innerText").lower(),
                        )
                    except:
                        pass
                    print("    " + span.get_attribute("innerText"))


def get_cocktails_tags_and_classes():
    browser = webdriver.Chrome(PATH_TO_DRIVER)
    browser.get("https://ru.inshaker.com/cocktails")
    for el in browser.find_elements_by_class_name("filter-select"):
        print(el.text)
        class_tag, created = ClassForCocktailTag.objects.get_or_create(
            class_name=el.text.lower()
        )
        for element in el.find_elements_by_class_name("list"):
            for div in element.find_elements_by_class_name("item"):
                for span in div.find_elements_by_tag_name("span"):
                    print("    " + span.get_attribute("innerText"))
                    try:
                        tag, created = TagForCocktail.objects.update_or_create(
                            class_name=class_tag,
                            tag_name=span.get_attribute("innerText").lower(),
                        )
                    except:
                        pass


def get_ing(url):
    new_browser = webdriver.Chrome(PATH_TO_DRIVER)
    new_browser.get(url)
    ing_name = new_browser.find_element_by_class_name("common-name").get_attribute(
        "innerText"
    )
    tags = []
    for tag in new_browser.find_elements_by_class_name("tags"):
        for name in tag.find_elements_by_class_name("tag"):
            tags.append(name.get_attribute("innerText"))
    # большая картинка /html/body/div[9]/div[1]/div[2]
    for ii in new_browser.find_elements_by_xpath("/html/body/div[9]/div[1]/div[2]"):
        o = ii.get_attribute("style")
    descrp = new_browser.find_element_by_id("goods-text").get_attribute("innerText")
    rege = "/uploads/.*\.jpg"
    regex = re.compile(rege)
    # print(o)
    help_url = "https://ru.inshaker.com"
    img = regex.findall(o)[0]
    img = help_url + img
    new_browser.close()
    return (ing_name, img, img, descrp, tags)


def get_tools(url):
    new_browser = webdriver.Chrome(PATH_TO_DRIVER)
    new_browser.get(url)
    ing_name = new_browser.find_element_by_class_name("common-name").get_attribute(
        "innerText"
    )
    # большая картинка /html/body/div[9]/div[1]/div[2]
    for ii in new_browser.find_elements_by_xpath("/html/body/div[9]/div[1]/div[2]"):
        o = ii.get_attribute("style")
    descrp = new_browser.find_element_by_id("goods-text").get_attribute("innerText")
    rege = "/uploads/.*\.jpg"
    regex = re.compile(rege)
    # print(o)
    help_url = "https://ru.inshaker.com"
    img = regex.findall(o)[0]
    img = help_url + img
    new_browser.close()
    return (ing_name, img, img, descrp)


def get_cocktails():
    browser = webdriver.Chrome(PATH_TO_DRIVER)
    browser.get("https://ru.inshaker.com/cocktails?random_page=15")
    count = 0
    for element in browser.find_elements_by_class_name("cocktail-item"):
        if count > 10:
            break
        for cocktail_before in element.find_elements_by_class_name(
            "cocktail-item-preview"
        ):

            smallImg = element.find_element_by_tag_name("img").get_attribute("src")

            # print(cocktail_before.get_attribute("href"))
            new_browser = webdriver.Chrome(PATH_TO_DRIVER)
            new_browser.get(cocktail_before.get_attribute("href"))

            # name
            cocktail_name = new_browser.find_element_by_class_name(
                "common-name"
            ).get_attribute("innerText")
            if Cocktail.objects.filter(name=cocktail_name):
                new_browser.close()
                continue

            # tags
            tags = []
            for tag in new_browser.find_elements_by_class_name("tags"):
                for name in tag.find_elements_by_class_name("tag"):
                    tags.append(name.get_attribute("innerText"))

            # ingredients
            ing_result = []
            for ul in new_browser.find_elements_by_class_name("ingredients"):
                for li in ul.find_elements_by_tag_name("li"):
                    for a in li.find_elements_by_class_name("common-good-icon"):
                        url = a.get_attribute("href")
                        for div in a.find_elements_by_class_name("icon"):
                            ing_result.append(get_ing(url))

            # tools
            tools_result = []
            for ul in new_browser.find_elements_by_class_name("tools"):
                for li in ul.find_elements_by_tag_name("li"):
                    for a in li.find_elements_by_class_name("common-good-icon"):
                        url = a.get_attribute("href")
                        for div in a.find_elements_by_class_name("icon"):
                            tools_result.append(get_ing(url))

            # для большой  картинки /html/body/div[9]/div[1]/div[3]
            for ii in new_browser.find_elements_by_xpath(
                "/html/body/div[9]/div[1]/div[3]"
            ):
                img = ii.get_attribute("style")
                print(img)
            print(smallImg)
            help_url = "https://ru.inshaker.com"
            regex = re.compile("/uploads/.*\.jpg")
            try:
                img = regex.findall(img)[0]
                img = help_url + img
            except:
                img = smallImg

            # steps
            steps = {}
            step_num = 0
            for step in new_browser.find_elements_by_class_name("steps"):
                for step_name in step.find_elements_by_tag_name("li"):
                    steps[str(step_num)] = step_name.get_attribute("innerText")
                    print(step_name.get_attribute("innerText"))
                    step_num += 1

            # steps = json.dumps(steps,ensure_ascii=False)

            # description
            about = ""
            for blockqoute in new_browser.find_elements_by_class_name("body"):
                for p in blockqoute.find_elements_by_tag_name("p"):
                    about = p.get_attribute("innerText")

            # measure и amount для ингридиентов и инструментов.
            m_arr = []
            a_arr = []
            m_and_a_for_ingredient = []
            m_and_a_for_tool = []
            i = 0
            for tabels in new_browser.find_elements_by_class_name("ingredient-tables"):
                for table in tabels.find_elements_by_tag_name("table"):

                    for a in table.find_elements_by_class_name("amount"):
                        a_arr.append(a.get_attribute("innerText"))
                    for m in table.find_elements_by_class_name("unit"):
                        m_arr.append(m.get_attribute("innerText"))

                    if i == 0:
                        j = 0
                        while j < len(m_arr):
                            m_and_a_for_ingredient.append((m_arr[j], a_arr[j]))
                            j += 1
                    else:
                        j = 0
                        while j < len(m_arr):
                            m_and_a_for_tool.append((m_arr[j], a_arr[j]))
                            j += 1

                    i += 1
                    m_arr.clear()
                    a_arr.clear()

            # модели для ингредиентов
            models_ing = []
            i = 0
            for result in ing_result:
                tag_models = []
                for tag_ in result[4]:
                    try:
                        tag_model, created = TagForIngredient.objects.get_or_create(
                            tag_name=tag_
                        )
                    except:
                        print("missed:  " + tag_)
                        continue
                    tag_models.append(tag_model)

                ing, created = Ingredient.objects.get_or_create(
                    name=result[0],
                    # img=requests.get(result[1]).content,
                    # small_img=requests.get(result[2]).content,
                    description=result[3],
                    measure=m_and_a_for_ingredient[i][0],
                )
                if created:
                    ing.cacheImg(result[1])
                    ing.cacheSmallImg(result[2])
                for tag__ in tag_models:
                    ing.ingredient_tag.add(tag__)

                # (ing_name, img, img, descrp, tags)
                models_ing.append(ing)
                i += 1

            # модели для инструментов
            tool_models = []
            for result in tools_result:
                # (ing_name, img, img, descrp, tags)
                tool, created = BarTool.objects.get_or_create(
                    name=result[0], description=result[3]
                )
                if created:
                    tool.cacheImg(result[1])
                    tool.cacheSmallImg(result[2])
                tool_models.append(tool)

            # сама сущность коктейль
            cocktail, created = Cocktail.objects.get_or_create(
                name=cocktail_name,
                description=about,
                recipe_text=steps,
            )
            cocktail.cacheImg(img)
            cocktail.cacheSmallImg(smallImg)
            # задаем теги коктейлю
            for cockt_tag in tags:
                try:
                    cockt_tag_model, created = TagForCocktail.objects.get_or_create(
                        tag_name=cockt_tag
                    )
                except:
                    print("missed cockt: " + cockt_tag)
                    continue
                cocktail.cocktail_tag.add(cockt_tag_model)

            # модель рецепта
            i = 0
            for ingredient_model in models_ing:
                obj, created = CocktailRecipe.objects.get_or_create(
                    cocktail=cocktail,
                    ingredient=ingredient_model,
                    amount=int(m_and_a_for_ingredient[i][1]),
                )
                i += 1

            # модель для таблицы cocktailTools
            i = 0
            for tool_model in tool_models:
                obj, created = CocktailTool.objects.get_or_create(
                    cocktail=cocktail,
                    tool=tool_model,
                    amount=int(m_and_a_for_tool[i][1]),
                )
                i += 1
            new_browser.close()
            i += 1
            count += 1
