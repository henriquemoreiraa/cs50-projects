export interface RootVerses {
  occurrence: number;
  version: string;
  verses: Verse[];
}

export interface RootChapter {
  book: Book;
  chapter: Chapter;
  verses: {
    number: number;
    text: string;
  }[];
}

export interface Verse {
  book: Book;
  chapter: number;
  number: number;
  text: string;
}

export interface Chapter {
  number: number;
  verses: number;
}

export interface Book {
  abbrev: Abbrev;
  author: string;
  chapters: number;
  group: string;
  name: string;
  testament: string;
}

export interface Abbrev {
  pt: string;
  en: string;
}
