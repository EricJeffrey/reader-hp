function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// 随机一个颜色值，返回 {name: x, color: x}
function randomColor() {
    let colors = [
        { name: "RED", color: "rgb(244, 67, 54) "},
        { name: "PINK", color: "rgb(233, 30, 99) "},
        { name: "PURPLE", color: "rgb(156, 39, 176) "},
        { name: "DEEP PURPLE", color: "rgb(103, 58, 183) "},
        { name: "INDIGO", color: "rgb(63, 81, 181) "},
        { name: "BLUE", color: "rgb(33, 150, 243) "},
        { name: "LIGHT BLUE", color: "rgb(3, 169, 244) "},
        { name: "CYAN", color: "rgb(0, 188, 212) "},
        { name: "TEAL", color: "rgb(0, 150, 136) "},
        { name: "GREEN", color: "rgb(76, 175, 80) "},
        { name: "LIGHT GREEN", color: "rgb(139, 195, 74) "},
        { name: "LIME", color: "rgb(205, 220, 57) "},
        { name: "AMBER", color: "rgb(255, 193, 7) "},
        { name: "ORANGE", color: "rgb(255, 152, 0) "},
        { name: "DEEP ORANGE", color: "rgb(255, 87, 34) "},
        { name: "BROWN", color: "rgb(121, 85, 72) "},
        { name: "GREY", color: "rgb(158, 158, 158) "},
        { name: "BLUE GREY", color: "rgb(96, 125, 139)" }
    ];
    let rand = Math.floor(Math.random() * colors.length);
    return colors[rand];
}