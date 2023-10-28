"use client";

import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState, RefObject } from 'react';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
  
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import saveAs  from 'file-saver';
import axios from 'axios';

const  predictpage =  () => {

    const [claim, setClaim] = useState('');
    const [showDiv, setShowDiv] = useState(false);
    const { createProxyMiddleware } = require('http-proxy-middleware');
    const [prediction, setPrediction] = useState('');
    const [evidence, setEvidence] = useState([]);
    const [alert, setAlert] = useState(false);
    const [html, setHtml] = useState('');
    const [loading, setLoading] = useState(false);
    const [iframeLoaded, setIframeLoaded] = useState(false);
    const [progress, setProgress] = useState('');
    
    async function highlight(texts: string[],htmlcode: string) {
        var a = htmlcode
        for(let i = 0; i < texts.length; i++) {
                const text = texts[i];
                a =  a.replace(text, `<mark id="evidence${i}">${text}</mark>`);}

        setHtml(a);
    }   
    
    async function handleCrawler(link : String) {
        const res = await fetch(`/api/crawler?url=${link}`);
        const html  = await res.json();
        setHtml(html);
        return html
    }
      
    async function handleSubmit(e: { preventDefault: () => void; target: any; }) {
        e.preventDefault();
        setLoading(true);
        const config = {
            headers:{
                 "Access-Control-Allow-Origin": "*"
            }
        };
        const url = "http://localhost:8000/predict";
        const data ={
            statement: ` ${claim} `
        }
        const resp = axios.post(url, data, config)
          .then(async res => {console.log(res['data']);setProgress(res['data']['softmax']) ;setPrediction(res['data']['label']);setEvidence(res['data']['evidence']);handleCrawler(res['data']['url']); highlight(res['data']['evidence'],await handleCrawler(res['data']['url']));setShowDiv(true);setLoading(false);setAlert(true)} )
          .catch(err => console.log(err))
    }
  
    return (  
        <div className="bg-white flex flex-row h-full max-w-screen-fit dark:white">
            {/* Bên trái nha */}
            <div className="dark:white bg-white border-r border-primary/15 fixed flex-none w-96 h-full mx-1" >
                <Card className="w-[350px] m-4">
                    <CardHeader>
                         <CardTitle>ViFactCheck</CardTitle>
                         {/* <CardDescription>Nhập các thông tin cần kiểm chứng.</CardDescription>  */}
                    </CardHeader>
                    <CardContent>
                        <form>
                            <div className="grid w-full items-center gap-4">
                                <div className="flex flex-col space-y-1.5">
                                <Input onChange={(event) => setClaim(event.target.value) } value={claim} id="name" placeholder="Nhập thông tin cần kiểm chứng..." />
                                </div>
                                <div className="flex flex-col space-y-1.5">
                                </div>
                            </div>
                            <div className="flex mt-1 justify-between">     
                                <Button type="reset" onClick={(event) => {setClaim("");setShowDiv(false);setPrediction("")}} variant="outline">Huỷ</Button>
                                <Button type="submit" id="submitbutton" onClick={(event)=> handleSubmit(event)}>                       
                                        <p>Kiểm chứng</p> 
                                        {loading && <span className="loading loading-spinner"></span>}
                                </Button>
                            </div>
                            <div className="mt-3">
                                <b >Câu tuyên bố bạn muốn kiểm chứng: </b>{claim}
                            </div>
                        </form>
                    </CardContent>
                </Card>
                {/* Cai nay la de hien cai label ha */}
                {prediction === 'Support' && (
                    <div className="alert alert-success w-[350px] mx-4">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>Thông tin đúng sự thật!</span>
                        <div className="radial-progress" style={{"--value":`${progress}`}}>{progress}%</div>
                    </div> 
                )}

                {prediction === 'Refuted' && (
                    <div className="alert alert-error w-[350px] mx-4">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>Thông tin sai sự thật!</span>
                        <div className="radial-progress" style={{"--value":`${progress}`}}>{progress}%</div>
                    </div>
                )}
                {prediction === 'NEI' && (
                    <div className="alert alert-warning w-[350px] mx-4">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                        <span>Chưa đủ thông tin để kết luận!</span>
                        <div className="radial-progress" style={{"--value":`${progress}`}}>{progress}%</div>
                    </div>
                )}
                <Card className="w-[350px] m-4" >
                    <CardHeader>
                        <CardTitle>Các Bằng chứng</CardTitle>
                    </CardHeader>
                    <CardContent>
                    <Accordion type="single" collapsible className="w-full">
                        <AccordionItem value="item-1">
                            <AccordionTrigger>Bằng chứng 1</AccordionTrigger>
                            <AccordionContent>
                                {evidence[0]}
                            </AccordionContent>
                        </AccordionItem>
                        <AccordionItem value="item-2">
                            <AccordionTrigger>Bằng chứng 2</AccordionTrigger>
                            <AccordionContent>
                                {evidence[1]}
                            </AccordionContent>
                        </AccordionItem>
                        <AccordionItem value="item-3">
                            <AccordionTrigger>Bằng chứng 3</AccordionTrigger>
                            <AccordionContent>
                                {evidence[2]}
                            </AccordionContent>
                        </AccordionItem>
                    </Accordion>

                    </CardContent>
                </Card>
            </div> 
            {/* Bên giua nha */}
            {showDiv &&<div suppressHydrationWarning id="content_div" className="w-1/3 pl-96 h-full dark:white bg-white">
                <div>
                    <iframe title="Highlighted Text" width="1500" height="1350" srcDoc={html} frameBorder="0"/>
                </div>  
            </div> }    
            
        </div>
    );
}

export default predictpage;
function setIframeLoaded(arg0: boolean) {
    throw new Error("Function not implemented.");
}

