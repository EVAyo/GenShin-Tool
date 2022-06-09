import { useState } from "react"
import { FaTimes } from "react-icons/fa"
import { AppButton } from "./AppButton"
import { SongActionButton } from "./SongActionButton"


interface FloatingDropdownProps {
    position?: "bottom"
    children: React.ReactNode
    tooltip?: string
    Icon: React.FC
    className?: string
    offset?: number
    style?: React.CSSProperties
    onClose?: () => void
}

export function FloatingDropdown({ 
        position = 'bottom', 
        children, 
        Icon, 
        className = "", 
        style = {}, 
        onClose, 
        tooltip, 
        offset = 3 
    }: FloatingDropdownProps) {
    const [isActive, setActive] = useState(false)
    return <div className={`${className} floating-dropdown ${isActive ? "floating-dropdown-active" : ""}`}>
        <SongActionButton style={{ margin: 0, ...style }}
            onClick={() => {
                setActive(!isActive)
                if (isActive && onClose) onClose()
            }}
            tooltip={tooltip}
        >
            {isActive
                ? <FaTimes />
                : <Icon />
            }
        </SongActionButton>

        <div
            className={`floating-children-${position}`}
            style={{ transform: `translateX(calc(-100% + ${offset}rem)` }}
        >
            {children}
        </div>
    </div>
}


interface FloatingDropdownButtonProps {
    children: React.ReactNode
    onClick?: () => void

}
interface FloatingDropdownTextProps {
    text: string
}

export function FloatingDropdownText({ text }: FloatingDropdownTextProps) {
    return <div className="floating-dropdown-text">
        {text}
    </div>
}
export function FloatingDropdownRow({ children, onClick }: FloatingDropdownButtonProps) {
    return <AppButton
        className='row row-centered'
        style={{ padding: "0.4rem", minWidth: "unset" }}
        onClick={onClick}
    >
        {children}
    </AppButton>
}