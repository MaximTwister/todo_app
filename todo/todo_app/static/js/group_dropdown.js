const paragraphEmptyTitle = document.getElementById("paragraph-empty-title")

const todo_cards = Array.prototype.filter.call(
    document.getElementsByTagName('div'),
    (el) => el.getAttribute('group_title')
)

const group_selector = document.getElementById("select_group")
group_selector.addEventListener("change",  (event) => {
    paragraphEmptyTitle.innerHTML = ''
    let selector = event.target
    let selectedGroupIndex = selector.selectedIndex
    let selectedGroupName = selector.options[selectedGroupIndex].value
    console.log(`Selected Group: ${selectedGroupName}`)
    showOnlySelectedGroups(selectedGroupName)
})


function showOnlySelectedGroups (selectedGroupName) {
    todo_cards.forEach( (div) => {
        let divGroupTitle = div.getAttribute("group_title")
        if (selectedGroupName === "all_groups" || divGroupTitle === selectedGroupName) {
            div.classList.remove('not-vis')
        } else {
            div.classList.add('not-vis')
        }
    })
    const cardsHidden = Array.prototype.filter.call(
    document.getElementsByTagName('div'),
    (el) => el.classList.contains('not-vis'))

    if (cardsHidden.length === todo_cards.length ) {
        showEmptyTitle(selectedGroupName)
    }
}

const showEmptyTitle = (selectedGroupName) => {
    let text = `No todos for group ${selectedGroupName}`
    let textNode = document.createTextNode(text)
    paragraphEmptyTitle.appendChild(textNode)
}


console.log(`TodoCards: ${todo_cards}`)
console.log(`Selector Index: ${group_selector.selectedIndex}`)
console.log(`GroupsSelectorOptions: ${group_selector.options[group_selector.selectedIndex].value}`)