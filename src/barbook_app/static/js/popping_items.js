function get_ingredients() {
    $.ajax({
        type: "GET",
        contentType: "application/json",
        url: "/api/ingredients",
        success: function (ret_data, textStatus, xhr) {
            ret_data.forEach(function (item) {
                $("#ingredient_append").append(
                    '<div class="ingred__block-photo create__ingred-photo--block">\n' +
                    '        <div class="ingred__block-item">\n' +
                    '            <a href="/ingredients/' + item['id'] + '" class="link_ingred">\n' +
                    '                <img src="' + item['small_img'] + '" class="ingred-img" alt="">\n' +
                    '                <div class="ingred__name create__ingred-name">' + item["name"] + '</div>\n' +
                    '            </a>\n' +
                    '            <div class="check__ing-block">\n' +
                    '                <input type="checkbox" value="' + item['id'] + '" name="ing_checkbox' + item['id'] + '" class="ingredient_check">\n' +
                    '                <input class="ing__count" id="ing_amount' + item['id'] + '" placeholder="' + item['measure'] + '">\n' +
                    '            </div>\n' +
                    '        </div>\n' +
                    '    </div>'
                );
            });
        }
    });
}

function get_bartools() {
    $.ajax({
        type: "GET",
        contentType: "application/json",
        url: "/api/bartools",
        success: function (ret_data, textStatus, xr) {
            ret_data.forEach(function (item) {
                $("#bartool_append").append(
                    '<div class="ingred__block-photo create__ingred-photo--block">\n' +
                    '        <div class="ingred__block-item">\n' +
                    '            <a href="#" class="link_ingred">\n' +
                    '                <img src="' + item['small_img'] + '" class="ingred-img" alt="">\n' +
                    '                <div class="ingred__name create__ingred-name">' + item['name'] + '</div>\n' +
                    '            </a>\n' +
                    '            <div class="check__ing-block">\n' +
                    '                <input type="checkbox" value="' + item['id'] + '" name="tool_checkbox' + item['id'] + '" class="tool_check">\n' +
                    '                <input type="text" id="tool_count' + item['id'] + '" class="ing__count" placeholder="шт">\n' +
                    '            </div>\n' +
                    '        </div>\n' +
                    '    </div>'
                );
            });
        }
    });
}

var num_of_inputs = 1;

function new_recipe_step_field() {
    num_of_inputs++;
    $("#step_append").append(
        '<input class="log recipe__text" type="text" name="' + num_of_inputs + '" id="step' + num_of_inputs + '" required>'
    )
}


function delete_recipe_step_field() {
    if (num_of_inputs === 1) {
    } else {
        $("#step" + num_of_inputs).remove();
        num_of_inputs--;
    }
}


function load_page() {
    get_bartools();
    get_ingredients();
}

function popping_from_form() {
    var user_id = $("#user_id").val();
    console.log(user_id)

    var name = $("#name").val();
    console.log(name);

    var about = $("#cocktail_info").val();
    console.log(about);

    var steps = {};
    for (i = 1; i <= num_of_inputs; i++) {
        steps[i] = $("#step" + i).val()
    }
    console.log(steps);

    var selected_ing = []
    $("input:checkbox[class=ingredient_check]:checked").each(
        function () {
            var ing_id = $(this).val();
            var amount = $("#ing_amount" + ing_id).val();
            selected_ing.push({"ingredient": ing_id, "amount": amount});
        }
    );
    console.log(selected_ing);

    var selected_tools = []
    $("input:checkbox[class=tool_check]:checked").each(
        function () {
            var tool_id = $(this).val();
            var count = $("#tool_count" + tool_id).val();
            var map = {"tool": tool_id, "amount": count};
            console.log(map);
            selected_tools.push(map);
        }
    );
    console.log(selected_tools);

    var cocktail = {
        "author_id": user_id,
        "name": name,
        "info": about,
        "recipe_text": steps,
        "ingredients": selected_ing,
        "bartools": selected_tools
    }

    console.log(cocktail);

    var small_img = $("#image_small").get(0).files[0];
    var img = $("#image_big").get(0).files[0];
    var form_data = new FormData();


    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    form_data.append("small_img", small_img);
    form_data.append("img", img);
    form_data.append("author", user_id);
    form_data.append("name", name);
    form_data.append("description", about);
    for (i = 0; i < selected_ing.length; i++) {
        form_data.append("recipe[" + i + "]ingredient", selected_ing[i]['ingredient']);
        form_data.append("recipe[" + i + "]amount", selected_ing[i]['amount']);
    }
    for (i = 0; i < selected_tools.length; i++) {
        console.log("seeeeelected_tools : " + selected_tools.toString())
        form_data.append("cocktail_tool[" + i + "]tool", selected_tools[i].tool);
        form_data.append("cocktail_tool[" + i + "]amount", selected_tools[i].amount);
    }
    form_data.append("recipe_text", JSON.stringify(steps));
    form_data.append("csrfmiddlewaretoken", csrf);

    console.log(form_data);

    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: "/api/cocktails/",
        data: form_data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 1000000,
        success: function (result, xr, _not_data_) {
            document.location.href("cocktails/");
        },
        error: function (result, xt, _not_data_) {
            console.log("error");
        }
    });
}