import {Preferences} from "@capacitor/preferences"


async function starWord(word: string) {
    const starredWords = await getStarredWords()
    if (!starredWords.includes(word)) {
        starredWords.push(word)
    } else {
        starredWords.splice(starredWords.indexOf(word), 1)
    }
    await Preferences.set({
        key: "bookmarks",
        value: JSON.stringify(starredWords)
    })
}

async function isWordStarred(word: string) {
    const starredWords = await getStarredWords()
    return starredWords.includes(word)
}

async function getStarredWords() {
    const response = await Preferences.get({
        key: "bookmarks"
    })
    return JSON.parse(response.value || "[]")
}

export {
    isWordStarred,
    starWord,
    getStarredWords
}
