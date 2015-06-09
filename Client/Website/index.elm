module Debates where

import Color (grey)
import Graphics.Element (..)
import Graphics.Input (button, customButton)
import List ((::), foldl, reverse, map)
import Http
import Http (Request, Response(..))
import Mouse
import Signal ( Channel
              , Signal
              , (<~)
              , (~)
              , constant
              , mergeMany
              , send
              , channel
              , subscribe
              )
import Signal
import Text (asText, plainText, leftAligned)
import Window
import Json.Decode ( Decoder
                   , (:=)
                   , decodeString
                   , list
                   , object2
                   , string
                   )
import Result (Result(..))

type View = View
        { action : Request String
        , render : Channel View
                -> (Int,Int)
                -> Response String
                -> Element
        }
type alias Action = Request String
type alias Renderer = Channel View
                   -> (Int,Int)
                   -> Response String
                   -> Element
type alias Renderer' a = Channel View
                      -> (Int,Int)
                      -> a
                      -> Element
type alias ViewRec = { action : Action, render : Renderer }
unView : View -> ViewRec
unView (View v) = v
getAction : View -> Action
getAction (View {action}) = action
getRender : View -> Renderer
getRender (View {render}) = render

constView : Element -> View
constView elem = View { action = Http.get ""
                      , render = always (always (always elem))
                      }

initialView : View
initialView = constView empty

main : Signal Element
main =
    let chan : Channel View
        chan = channel initialView
        views : Signal View
        views = subscribe chan
        body : Signal Element
        body = Signal.map getRender views
             ~ constant chan
             ~ Window.dimensions
             ~ Http.send (Signal.map getAction views)
    in flow down <~ combine
       [ (navBar chan << fst) <~ Window.dimensions
       , body
       ]

combine : List (Signal a) -> Signal (List a)
combine = Signal.map reverse
       << foldl (\x z -> (::) <~ x ~ z) (constant [])

navBar : Channel View -> Int -> Element
navBar chan w =
    let h = 40 
        background = color grey << container w h topLeft
    in background <| flow right
       (  logoButton h chan
       :: spacer 20 h
       :: groupButtons h chan
       )

groupButtons : Int -> Channel View -> List Element
groupButtons h chan =
    let button' view label =
        let elem = plainText label
        in container (widthOf elem) h middle <|
           textButton chan view label
    in [ button' debateList  "Debates"
       , spacer 20 h
       , button' teamList "Teams"
       , spacer 20 h
       , button' debaterList "Debaters"
       , spacer 20 h
       , button' judgeList   "Judges"
       , spacer 20 h
       , button' teacherList "Teachers"
       ]

textButton : Channel a -> a -> String -> Element
textButton chan x label =
    let elem = plainText label
    in customButton (send chan x) elem elem elem

logoButton : Int -> Channel View -> Element
logoButton h chan =
    let logoImage = image (h * 481 // 400) h logoUrl
    in customButton (send chan initialView) logoImage
                    logoImage logoImage
logoUrl : String
logoUrl = "images/cougar.png"

type alias User = { name : String, email : String }
mkUser : String -> String -> User
mkUser n e = { name = n, email = e }
userListRenderer : Renderer
userListRenderer =
    let itemDecoder : Decoder User
        itemDecoder = object2 mkUser
                ("name"  := string)
                ("email" := string)
        itemRenderer : Renderer' User
        itemRenderer chan dims user = plainText
                <| "Name: " ++ user.name
                ++ " Email: " ++ user.email
    in listHandler itemDecoder itemRenderer


debaterList : View
debaterList =
    let url = "/api/users"
    in View {action = Http.get url, render = always (always asText) }
    {-
    in View {action = Http.get url, render = userListRenderer}
    -}

judgeList : View
judgeList =
    let url = "/api/users"
    in View {action = Http.get url, render = userListRenderer}

teacherList : View
teacherList =
    let url = "/api/users"
    in View {action = Http.get url, render = userListRenderer}

listHandler : Decoder a -> Renderer' a -> Renderer
listHandler dec rend =
    let listOf : Renderer' a -> Renderer' (List a)
        listOf renderer chan dims vs =
            flow down <| map (renderer chan dims) vs
    in handler (list dec) (listOf rend)

handler : Decoder a -> Renderer' a -> Renderer
handler decoder renderer' chan dims resp = case resp of
    Failure code err -> httpError code err
    Waiting          -> loading
    Success s        -> case decodeString decoder s of
        Err err -> decodeError err
        Ok  val -> renderer' chan dims val

httpError : Int -> String -> Element
httpError code err = plainText
                  <| "Error " ++ toString code ++ ": " ++ err
loading : Element
loading = plainText "Hold on a minute"
decodeError : String -> Element
decodeError err = plainText
        <| "Error while decoding server response: " ++ err

debateList : View
debateList = constView <| asText "Debate"

teamList : View
teamList = constView <| asText "Team"
