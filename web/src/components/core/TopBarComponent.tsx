"use client"

import classNames from "classnames";
import Link from "next/link";
import {usePathname} from "next/navigation";


type NavLink = {
    label: string;
    href: string;
}

const navLinks: NavLink[] = [
    {label: "Chat", href: "/chat"},
    {label: "Stats", href: "/stats"},
]


export function TopBarComponent() {

    const pathName = usePathname();


    return <div className="z-50 flex h-16 w-full items-center justify-start bg-zinc-900">

        <nav className="flex w-full max-w-6xl items-start justify-start px-4 gap-6">
            <div className="flex">
                <h1 className="text-2xl font-bold text-white">Orag</h1>
            </div>
            <div className="flex gap-2 items-center pt-2">
                {navLinks.map((link, i) => {
                    const isActive = pathName === link.href || pathName.startsWith(`${link.href}/`);

                    const linkClass = classNames({
                        "cursor-pointer hover:text-blue-500": true,
                        "text-zinc-400": !isActive,
                        "text-blue-500": isActive,
                    });


                    return <Link key={i} href={link.href} className={linkClass}>{link.label}</Link>
                })}
            </div>

        </nav>

    </div>;
}