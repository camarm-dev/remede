function starWord(word: string) {
    const starredWords = JSON.parse(localStorage.getItem("userStars") || "[]") as Array<string>
    if (!starredWords.includes(word)) {
        starredWords.push(word)
    } else {
        starredWords.splice(starredWords.indexOf(word), 1)
    }
    localStorage.setItem("userStars", JSON.stringify(starredWords))
}

function isWordStarred(word: string) {
    const starredWords = JSON.parse(localStorage.getItem("userStars") || "[]") as Array<string>
    return starredWords.includes(word)
}

function getStarredWords() {
    return JSON.parse(localStorage.getItem("userStars") || "[]")
}

export {
    isWordStarred,
    starWord,
    getStarredWords
}
