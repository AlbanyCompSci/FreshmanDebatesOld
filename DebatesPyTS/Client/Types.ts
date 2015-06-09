module Types {

interface FromJson<T> {
    fromJson(o : Object) : T;
}

interface ToJson<T> {
    toJson(v : T) : Object;
}

export enum DebateItem {
    SpeakerA,
    SpeakerB,
    CrossExam,
    SlideShow,
    Rebuttal,
    Argument
}

export class datetime {
    year   : number;
    month  : number;
    day    : number;
    hour   : number;
    minute : number;
    second : number;
}

export class Debate {
    title     : string; 
    time      : datetime;
    location  : string;
    judges    : number[]; // user ids
    affTeam   : number;   // team id
    negTeam   : number;
    affScores : [jid : number] : number; // key: judge id, value: score id
    negScores : [jid : number] : number;
}

export class Evaluation {
    score : number;
    notes : string;
}

export class Score {
    fields : [eid : DebateItem] : number; // key: debate item, value: evaluation id
}

export class Team {
    teachers : number[]; // user ids
    students : number[];
}

export class User {
    firstName : string;
    lastName  : string;
    email     : string;
}

}
