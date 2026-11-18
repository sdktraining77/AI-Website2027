import {Document} from "llamaindex"; // جسر بين الداتا تبعتي وال llm 
import * as fs from "node:fs/promises";   //للتعامل مع الملفات وقرائتها 
import {SentenceSplitter} from "llamaindex"; // لتقسيم النصوص الكبيرة الي نصوص صغيرة    

async function main() {
    const documents = await loadDoc();
    const splitter = new SentenceSplitter();}
    
//reading the file name 
async function loadDoc(): Promise<Document[]> {
    const documents: Document[] = [];
    const filename = await fs.readdir("./data");
    for (const doc of filename) {
        const content = await fs.readFile(`./data/${doc}`, "utf-8");
        new Document({text: content, metadata: {source: doc}});
        documents.push(new Document({text: content, metadata: {source: doc}}));
       
    }
    console.log("Documents loaded successfully.");
    console.log(documents);
    return documents;

}
loadDoc()
