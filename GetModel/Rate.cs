using System;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    public record Rate<T>
    {
        public T? Id { get; set; }
        public double Value { get; set; }
    }
}
