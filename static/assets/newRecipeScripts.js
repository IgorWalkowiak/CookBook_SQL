var ingredientsNumber = 1;
var stepsNumber =1;

function removeIngredient(){
    var parent = document.getElementById("ingredient"+(ingredientsNumber-1));
    parent.parentNode.removeChild(parent);
    if(ingredientsNumber > 1)
    {
        ingredientsNumber = ingredientsNumber-1;
    }
}

function removeStep(){
    var parent = document.getElementById("step"+(stepsNumber-1));
    parent.parentNode.removeChild(parent);
    if(stepsNumber > 1)
    {
        stepsNumber = stepsNumber-1;
    }
}

function addIngredient() {
    try {
    var ingredientDiv = document.createElement("div");
    ingredientDiv.setAttribute('id', "ingredient"+ingredientsNumber);
    ingredientDiv.setAttribute('class', 'ingredient');
    var parent = document.getElementById("ingredients");
    parent.appendChild(ingredientDiv);
    
    
    var text1 = document.createElement("input");
    text1.setAttribute('type', 'text');
    text1.setAttribute('id', "ingredientName"+ingredientsNumber);
    text1.setAttribute('name', "ingredientName"+ingredientsNumber);

    var label1 = document.createElement("label");
    label1.innerHTML="<br> Składnik: "+ ingredientsNumber+"<br> Nazwa:";
    label1.setAttribute('for', "ingredientName"+ingredientsNumber);
    label1.setAttribute('value', "ingredientName"+ingredientsNumber);


    var ingredientDiv1 = document.getElementById("ingredient"+ingredientsNumber);
    ingredientDiv1.appendChild(label1);
    ingredientDiv1.appendChild(text1);


    var text2 = document.createElement("input");
    text2.setAttribute('type', 'text');
    text2.setAttribute('form', 'form1');
    text2.setAttribute('id', "ingredientUnit"+ingredientsNumber);
    text2.setAttribute('name', "ingredientUnit"+ingredientsNumber);
    text2.setAttribute('class', 'integrate');

    var label2 = document.createElement("label");
    label2.innerHTML="<br> Jednostka:";
    label2.setAttribute('for', "ingredientUnit"+ingredientsNumber);
    label2.setAttribute('value', "ingredientUnit"+ingredientsNumber);


    ingredientDiv.appendChild(label2);
    ingredientDiv.appendChild(text2);

    var text3 = document.createElement("input");
    text3.setAttribute('type', 'text');
    text3.setAttribute('form', 'form1');
    text3.setAttribute('id', "ingredientAmount"+ingredientsNumber);
    text3.setAttribute('name', "ingredientAmount"+ingredientsNumber);
    text3.setAttribute('class', 'integrate');

    var label3 = document.createElement("label");
    label3.innerHTML="<br> Ilość:";
    label3.setAttribute('for', "ingredientAmount"+ingredientsNumber);
    label3.setAttribute('value', "ingredientAmount"+ingredientsNumber);
    ingredientDiv.appendChild(label3);
    ingredientDiv.appendChild(text3);
    }
    catch(err)
    {
        document.getElementById("errors").innerHTML = err.message;
    }

    ingredientsNumber = ingredientsNumber+1;

}

function addStep() {
try{
    var stepDiv = document.createElement("div");
    stepDiv.setAttribute('id', "step"+stepsNumber);
    stepDiv.setAttribute('class', 'step');
    var parent = document.getElementById("steps");
    parent.appendChild(stepDiv);

    var textarea = document.createElement("textarea");
    textarea.setAttribute('rows', '4');
    textarea.setAttribute('cols', '60');
    textarea.setAttribute('form', 'form1');
    textarea.setAttribute('id', "stepInput"+stepsNumber);
    textarea.setAttribute('name', "stepInput"+stepsNumber);
    textarea.setAttribute('class', 'steps');

    var label = document.createElement("label");
    label.innerHTML="<br> Krok: "+ stepsNumber;
    label.setAttribute('for', "stepInput"+stepsNumber);
    label.setAttribute('value', stepsNumber);


    stepDiv.appendChild(label);
    stepDiv.appendChild(textarea);
    stepsNumber = stepsNumber+1;
}
catch(err)
{
    document.getElementById("errors").innerHTML = err.message;
}
}
