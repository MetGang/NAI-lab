// Patryk Kośmider s16863
// Krzysztof Marek s16663
// 
// Gra: Kołko i krzyżyk
// Reguły: https://pl.wikipedia.org/wiki/K%C3%B3%C5%82ko_i_krzy%C5%BCyk

// Element HTML będący polem na planszy gry
let areas = Array.from(Array(9).keys()).map(elem => document.getElementById(`area-${elem}`))

// Zmienna określająca czy sztuczna inteligencja rozpoczyna grę
let aiStarted

// Zmienna odpowiedzialna za identyfikację obecnej rundy (X lub O)
let round

// Zmienna "pilnująca" czy gra wciąż trwa
let gameover = true

// Tablica możliwych ułożeń na planszy zapewniających wygraną
let boardCombos = [
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ],
]

// Przypisanie logiki gracza do eventu kliknięcia pola
areas.forEach((elem, index) => {
    elem.onclick = () => { playerAction(index) }
})

/**
 * Logika gracza
 * @param {*} index - indeks klikniętego pola na planszy
 */
function playerAction(index)
{
    if (!gameover && areas[index].textContent == '')
    {
        clickArea(index, 'human')

        if (!gameover)
        {
            aiAction()
        }
    }
}

// Logika sztucznej inteligencji
function aiAction()
{
    let aiChar = round ? 'X' : 'O'
    let playerChar = round ? 'O' : 'X'
    let aiCombosSize = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
    let playerCombosSize = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
    let chosen = null

    boardCombos.forEach((combo, index) => {
        combo.forEach((elem) => {
            if (areas[elem].textContent == aiChar) aiCombosSize[index]++
            if (areas[elem].textContent == playerChar) playerCombosSize[index]++
        })
    })

    aiCombosSize.forEach((size, index) => {
        if (size == 2 && chosen == null) boardCombos[index].forEach((elem) => {
            if (areas[elem].textContent == '' && chosen == null) chosen = elem
        })
    })

    if (chosen == null)
    {
        playerCombosSize.forEach((size, index) => {
            if (size == 2 && chosen == null) boardCombos[index].forEach((elem) => {
                if (areas[elem].textContent == '' && chosen == null) chosen = elem
            })
        })
    }

    if (chosen == null)
    {
        aiCombosSize.forEach((size, index) => {
            if (size == 1 && playerCombosSize[index] == 0 && chosen == null)
            {
                chosen = Math.max(...boardCombos[index])

                if (areas[chosen].textContent != '') chosen = Math.min(...boardCombos[index])
            }
        })
    }

    if (chosen == null) 
    {
        if (!aiStarted && areas[4].textContent == '')
            chosen = 4
        else if (areas[0].textContent == '')
            chosen = 0
        else if (areas[8].textContent == '')
            chosen = 8
        else
            areas.forEach((elem, index) => {
                if (elem.textContent == '') { chosen = index }
            })
    }

    clickArea(chosen, 'ai')
}

/**
 * Logika kliknięcia w pole
 * @param {*} index - indeks klikniętego pola
 * @param {*} player - oznaczenie gracza, który wykonał ruch
 */
function clickArea(index, player)
{
    areas[index].textContent = round ? 'X' : 'O'
    areas[index].style.cursor = 'not-allowed'

    let result = checkWinCondtion()

    if (result !== null)
    {
        if (result !== false)
        {
            result.forEach((value) => {
                areas[value].style.backgroundColor = player == 'ai' ? '#f004' : '#0f04'
            })
        }

        areas.forEach((elem) => {
            elem.style.cursor = 'not-allowed'
        })

        gameover = true
    }

    round = !round
}

/**
 * Sprawdzanie stanu planszy (wygrana, remis, gra wciąż trwa)
 * Zwraca:
 * - tablicę zawierającą indeksy pól tworzących linię w przypadku wygranej,
 * - fałsz w przypadku trwającej rozgrywki
 * - null w każdym innym przypadku
 */
function checkWinCondtion()
{
    if (areas[0].textContent != '' && areas[0].textContent == areas[1].textContent && areas[1].textContent == areas[2].textContent) return [ 0, 1, 2 ]
    if (areas[3].textContent != '' && areas[3].textContent == areas[4].textContent && areas[4].textContent == areas[5].textContent) return [ 3, 4, 5 ]
    if (areas[6].textContent != '' && areas[6].textContent == areas[7].textContent && areas[7].textContent == areas[8].textContent) return [ 6, 7, 8 ]
    if (areas[0].textContent != '' && areas[0].textContent == areas[3].textContent && areas[3].textContent == areas[6].textContent) return [ 0, 3, 6 ]
    if (areas[1].textContent != '' && areas[1].textContent == areas[4].textContent && areas[4].textContent == areas[7].textContent) return [ 1, 4, 7 ]
    if (areas[2].textContent != '' && areas[2].textContent == areas[5].textContent && areas[5].textContent == areas[8].textContent) return [ 2, 5, 8 ]
    if (areas[0].textContent != '' && areas[0].textContent == areas[4].textContent && areas[4].textContent == areas[8].textContent) return [ 0, 4, 8 ]
    if (areas[2].textContent != '' && areas[2].textContent == areas[4].textContent && areas[4].textContent == areas[6].textContent) return [ 2, 4, 6 ]

    if (areas.every(elem => elem.textContent != '')) return false

    return null
}

// Rozpoczęcie gry, "wyzerowanie" zmiennych
function startGame()
{
    areas.forEach((elem) => {
        elem.textContent = ''
        elem.style.backgroundColor = '#0000'
        elem.style.cursor = 'pointer'
    })

    round = true
    gameover = false
    aiStarted = document.getElementById('aiStarts').checked

    if (aiStarted) aiAction()
}
