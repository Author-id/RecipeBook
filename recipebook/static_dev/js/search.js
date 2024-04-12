const inp_name = document.getElementById("search-name");
const inp_category = document.getElementById("search-category");
const inp_level = document.getElementById("search-level");
const btn = document.getElementById("search-btn");
const clear_btn = document.getElementById("search-clear-btn");

const ingredient_container = document.getElementById("search-ingredient-container");
const ingredient_include = document.getElementById("search-ingredient-include");
const ingredient_exclude = document.getElementById("search-ingredient-exclude");
const ingredient_input = document.getElementById("search-ingredient-input");
const ingredient_list = document.getElementById("search-ingredient-list");

ingredient_input.addEventListener("focus", () => ingredient_list.classList.add("search_visible"))
window.addEventListener("click", e =>
{
	let el = e.target;
	let found = false;
	while (el)
	{
		if (el == ingredient_container)
		{
			found = true;
			break
		}
		el = el.parentElement
	}
	if (!found)
		ingredient_list.classList.remove("search_visible");
})
window.addEventListener("keyup", e =>
{
	if (e.key == "Escape")
		ingredient_list.classList.remove("search_visible");
})
ingredient_input.addEventListener("input", () =>
{
	ingredient_list.classList.add("search_visible");
	const search = ingredient_input.value.trim().toLowerCase().replaceAll(/\s+/g, " ");
	let found = false;
	for (let i = 0; i < ingredient_list.children.length - 1; i++)
	{
		const el = ingredient_list.children[i];
		if (el.children[0].innerText.toLowerCase().includes(search))
		{
			el.style.display = "";
			found = true;
		}
		else
			el.style.display = "none";
	}
	const not_found_el = ingredient_list.children[ingredient_list.children.length - 1];
	not_found_el.style.display = found ? "none" : "";
})

const url = new URL(window.location);
inp_name.value = url.searchParams.get("sn");
inp_category.value = url.searchParams.get("sc");
inp_level.value = url.searchParams.get("sl");

let ingredients_include = url.searchParams.get("si")?.split("-").filter(v => v && !isNaN(+v)) || [];
let ingredients_exclude = url.searchParams.get("sie")?.split("-").filter(v => v && !isNaN(+v)) || [];


for (let i = 0; i < ingredient_list.children.length - 1; i++)
{
	const el = ingredient_list.children[i];
	const id = el.getAttribute("data-id");
	const name = el.children[0].innerText
	const cbx_include = el.querySelector("#search-ingredient-include-chb")
	const cbx_exclude = el.querySelector("#search-ingredient-exclude-chb")
	const include_i = ingredients_include.indexOf(id);
	const exclude_i = ingredients_exclude.indexOf(id);
	if (include_i >= 0)
	{
		ingredients_include[include_i] = { id, name };
		cbx_include.checked = true;
	}
	if (exclude_i >= 0)
	{
		ingredients_exclude[exclude_i] = { id, name };
		cbx_exclude.checked = true;
	}
	cbx_include.addEventListener("change", () =>
	{
		const i = ingredients_include.findIndex(v => v.id == id);
		if (cbx_include.checked)
		{
			if (i < 0) ingredients_include.push({ id, name });

			cbx_exclude.checked = false;
			const i2 = ingredients_exclude.findIndex(v => v.id == id);
			if (i2 >= 0) ingredients_exclude.splice(i2, 1);
		}
		else
		{
			ingredients_include.splice(i, 1);
		}
		displayAllIngredients();
	});
	cbx_exclude.addEventListener("change", () =>
	{
		const i = ingredients_exclude.findIndex(v => v.id == id);
		if (cbx_exclude.checked)
		{
			if (i < 0) ingredients_exclude.push({ id, name });

			cbx_include.checked = false;
			const i2 = ingredients_include.findIndex(v => v.id == id);
			if (i2 >= 0) ingredients_include.splice(i2, 1);
		}
		else
		{
			ingredients_exclude.splice(i, 1);
		}
		displayAllIngredients();
	});
}

function displayIngredients(container, ingredients)
{
	container.innerHTML = "";
	for (const ingredient of ingredients)
	{
		const el = document.createElement("span");
		el.innerText = ingredient.name;
		container.appendChild(el);
	}
}
function displayAllIngredients()
{
	displayIngredients(ingredient_include, ingredients_include);
	displayIngredients(ingredient_exclude, ingredients_exclude);
}
displayAllIngredients()

clear_btn.addEventListener("click", () =>
{
	inp_name.value = "";
	inp_category.value = "";
	inp_level.value = "";
	ingredients_include = [];
	ingredients_exclude = [];
})


btn.addEventListener("click", () =>
{
	const url = new URL(window.location);
	url.searchParams.set("sn", inp_name.value);
	url.searchParams.set("sc", inp_category.value);
	url.searchParams.set("sl", inp_level.value);
	url.searchParams.set("si", ingredients_include.map(v => v.id).join("-"));
	url.searchParams.set("sie", ingredients_exclude.map(v => v.id).join("-"));
	window.location = url;
})


