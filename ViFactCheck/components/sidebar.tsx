    "use client";

    import { Home, Search, LayoutDashboard } from "lucide-react";
    import { usePathname, useRouter } from "next/navigation";

    import { cn } from "@/lib/utils";

    export const Sidebar = () => {
        const pathname = usePathname();
        const router = useRouter();
        const routes =[
            {
                icon: Home,
                href: "/",
                label: "Home",
                admin: false
            },
            {
                icon: Search,
                href: "/predict",
                label: "Predict",
                admin: false
            },
            {
                icon: LayoutDashboard,
                href: "/dashboard",
                label: "Dashboard",
                admin: true
            },
        ];
        const onNavigate = (url: string ,admin: boolean) =>{
            //check if admin
            return router.push(url)
        }

        return (
            <div className="flex h-full text-primary bg-background">
                <div className="p-2 flex flex-1 justify-center">
                    <div className="space-x-4 flex items-center">
                        {routes.map((route) => (
                            <div
                                onClick={() => onNavigate(route.href, route.admin)}
                                key={route.href}
                                className={cn(
                                    "text-muted-foreground text-xs group flex p-3 justify-center font-medium cursor-pointer hover:text-primary hover:bg-primary/10 rounded-lg transition", pathname === route.href && "bg-primary/10 text-primary"
                                )}
                            >
                                <div className="flex flex-row gap-x-2 items-center">
                                    <route.icon className="h-5 w-5" />
                                    {route.label}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        )
    }