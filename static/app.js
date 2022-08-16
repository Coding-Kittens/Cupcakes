
addCakeForm = $(".add_cake");
cakesList = $("#cupcakes_list");

//deletes a cupcake when button is pressed
$("ul").on("click", "button", async function () {
  const res = await axios.delete(
    `http://127.0.0.1:5000/api/cupcakes/${$(this).data("id")}`
  );
  $(this).parent().remove();
});

//adds the html for a cupcake
function addCupcake(cake) {
  new_li = $(`<li></li>`);
  new_p = $(
    `<p> Flavor ${cake.flavor}, Size ${cake.size}, Rating ${cake.rating} </p>`
  );
  new_img = $(`<img src="${cake.image}">`);
  new_btn = $(
    `<button data-id="${cake.id}" type="button" name ='button'class='delete'>X</button>`
  );

  new_li.append(new_p);
  new_li.append(new_img);
  new_li.append(new_btn);
  cakesList.append(new_li);
}

//gets and shows a list of all cupcakes
async function listAllCakes() {
  const res = await axios.get("http://127.0.0.1:5000/api/cupcakes");
  const cakeList = res.data.cupcakes;

  for (let cake in cakeList) {
    addCupcake(cakeList[cake]);
  }
}

//adds a cupcake
addCakeForm.on("submit", async function (evt) {
  evt.preventDefault();
  const cake = await axios.post(
    "http://127.0.0.1:5000/api/cupcakes",
    {
      flavor: $("input[name='flavor']").val(),
      size: $("input[name='size']").val(),
      rating: $("input[name='rating']").val(),
      image: $("input[name='image']").val(),
    },
    "application/json;charset=UTF-8"
  );
  $("input[name='flavor']").val("");
  $("input[name='size']").val("");
  $("input[name='rating']").val("");
  $("input[name='image']").val("");

  addCupcake(cake.data.cupcake);
});

listAllCakes();
