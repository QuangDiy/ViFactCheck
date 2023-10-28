"use client";

import { UserButton } from "@clerk/nextjs";
import { Menu } from "lucide-react";
import Link from "next/link";
  
import { ModeToggle } from "./mode-toggle";
import { MobileSidebar } from "./mobile-sidebar";
import { Sidebar } from "./sidebar";



export const Navbar = () => {
    return (
        <div className="fixed w-full z-50 flex justify-between items-center py-2 px-4 border-b border-primary/15 bg-background h-16">
            <div className="flex items-center">
                {/* <MobileSidebar /> */}
                <Link href="/">
                    <h1 className="hidden md:block text-xl md:text-3xl font-bold text-primary"> 
                        ViFactCheck
                    </h1>
                </Link>
            </div>
            <div className="flex items-center gap-x-3">
                <Sidebar/>
                <ModeToggle />
                <UserButton /> 
            </div>
        </div>
    );
};