namespace DGP.Genshin.FPSUnlocking
{
    public enum UnlockResult
    {
        /// <summary>
        /// 解锁成功，且游戏已经顺利运行完成
        /// </summary>
        Ok,
        /// <summary>
        /// 
        /// </summary>
        ProcessIsNull,
        ProcessHasExited,
        ModuleSearchTimeExceed,
        ReadProcessMemoryFailed,
        NoMatchedPatternFound,
        UnlockerInvalid
    }
}