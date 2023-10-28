import { Navbar } from "@/components/navbar";
const RootLayout = ({
    children
}:{
    children: React.ReactNode;
}) => {
    return ( 
        <div suppressHydrationWarning className="h-screen">
            <Navbar />
            <main className="pt-16 h-full">
                {children}
            </main>
        </div>
     ); 
}
 
export default RootLayout;