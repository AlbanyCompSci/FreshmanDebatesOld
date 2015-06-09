main : Signal Element
main = flow down <~ mergeMany
        [ header
        , menu
        , body
        ]

header : Signal Element
header = 
