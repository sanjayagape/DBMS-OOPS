import { Component, type ReactNode, lazy, Suspense, useEffect } from 'react'
import { BrowserRouter, Link, Route, Routes, useLocation } from 'react-router-dom'
import { MotionConfig, motion, useReducedMotion } from 'motion/react'
import { AppProvider, useApp } from './hooks/useApp'
import { Layout } from './components/Layout'
import { Empty, Loading } from './components/ui'
import { Home } from './pages/Home'
const Explore = lazy(() => import('./pages/Explore').then(m => ({ default:m.Explore })))
const Donate = lazy(() => import('./pages/Donate').then(m => ({ default:m.Donate })))
const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default:m.Dashboard })))
const Tracking = lazy(() => import('./pages/Tracking').then(m => ({ default:m.Tracking })))
const Impact = lazy(() => import('./pages/Impact').then(m => ({ default:m.Impact })))
const Auth = lazy(() => import('./pages/Auth').then(m => ({ default:m.Auth })))
const Profile = lazy(() => import('./pages/Auth').then(m => ({ default:m.Profile })))
const Onboarding = lazy(() => import('./pages/Onboarding').then(m => ({ default:m.Onboarding })))
class ErrorBoundary extends Component<{ children:ReactNode },{ failed:boolean }> {
  state = { failed:false }; static getDerivedStateFromError() { return { failed:true } }
  render() { return this.state.failed ? <div className="container page"><Empty title="Let’s try a fresh start." action={<button className="button primary" onClick={() => window.location.reload()}>Reload FoodBridge</button>}>The page could not load. Your saved demo activity stays in this browser.</Empty></div> : this.props.children }
}
function Page({ children }: { children:ReactNode }) { const location = useLocation(); const reduced = useReducedMotion(); useEffect(() => { const titles: Record<string,string> = { '/':'Good food brings people closer','/explore':'Explore food','/donate':'Share food','/dashboard':'Your dashboard','/impact':'Our impact','/login':'Welcome back','/register':'Join the community','/profile':'Your profile','/onboarding':'Welcome to FoodBridge' }; document.title = `${titles[location.pathname] ?? 'Follow the good'} · FoodBridge` },[location.pathname]); return <motion.div key={location.pathname} initial={{ opacity:reduced ? 1 : .4 }} animate={{ opacity:1 }} transition={{ duration:.2 }}>{children}</motion.div> }
function AppRoutes() { const { error,reload } = useApp(); if (error) return <div className="container page"><Empty title="The demo couldn’t load." action={<button className="button primary" onClick={reload}>Try again</button>}>{error}</Empty></div>; return <Suspense fallback={<Loading/>}><Routes><Route element={<Layout/>}><Route index element={<Page><Home/></Page>}/><Route path="explore" element={<Page><Explore/></Page>}/><Route path="donate" element={<Page><Donate/></Page>}/><Route path="dashboard" element={<Page><Dashboard/></Page>}/><Route path="tracking/:id" element={<Page><Tracking/></Page>}/><Route path="impact" element={<Page><Impact/></Page>}/><Route path="login" element={<Page><Auth mode="login"/></Page>}/><Route path="register" element={<Page><Auth mode="register"/></Page>}/><Route path="forgot-password" element={<Page><Auth mode="forgot"/></Page>}/><Route path="profile" element={<Page><Profile/></Page>}/><Route path="onboarding" element={<Page><Onboarding/></Page>}/><Route path="*" element={<div className="container page"><Empty title="This path could use a little redirect." action={<Link className="button primary" to="/">Back home</Link>}>The page you’re looking for isn’t here.</Empty></div>}/></Route></Routes></Suspense> }
export default function App() { return <ErrorBoundary><MotionConfig reducedMotion="user"><AppProvider><BrowserRouter><AppRoutes/></BrowserRouter></AppProvider></MotionConfig></ErrorBoundary> }
