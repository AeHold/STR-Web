// class Text {
//     constructor(title, author) {
//     this.title = title;
//     this.author = author;
//     }

//     getTitle() {
//     return this.title;
//     }

//     getAuthor (){
//     return this.author;
//     }

//     getAuthor = authorDecorator(this.getAuthor)
// }

// class Poem extends Text {
//     constructor(title, author, genre) {
//     super(title, author);
//     this.genre = genre;
//     }

//     getGenre() {
//     return this.genre;
//     }
// }


// function authorDecorator(descriptor) {
//     const originalMethod = descriptor;

//     descriptor = function () {
//     const author = originalMethod.call(this);
//     return `${author} ...`;
//     };

//     return descriptor;
// }

/*======================================================= */

function Text(title, author) {
    this.title = title;
    this.author = author;
}

Text.prototype.getTitle = function () {
    return this.title;
};

Text.prototype.getAuthor = function () {
    return this.author;
};


function Poem(title, author, genre) {
    Text.call(this, title, author);

    this.genre = genre;
}

Poem.prototype = Object.create(Text.prototype);

Poem.prototype.constructor = Poem;

Poem.prototype.getGenre = function () {
    return this.genre;
};

function authorDecorator(fn) {
    return function () {
    const author = fn.call(this);
    return `${author} ...`;
    };
}

Text.prototype.getAuthor = authorDecorator(Text.prototype.getAuthor);

/*==============================================================*/

const Text = new Text("Introduction to Cinema", 120);
console.log("Text Title:", Text.getTitle());
console.log("Text author:", Text.getAuthor());

const Poem = new Poem("Inception", 180, "Sci-Fi");
console.log("Poem Title:", Poem.getTitle());
console.log("Poem author:", Poem.getAuthor());
console.log("Poem Genre:", Poem.getGenre());